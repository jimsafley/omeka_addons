import ConfigParser
import json
import addonregistry
import os
import requests
import sqlite3
import time
import zipfile

print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + ' - Processing releases:'

inipath_map = {
    'classic_plugin': '/plugin.ini',
    'classic_theme': '/theme.ini',
    's_module': '/config/module.ini',
    's_theme': '/config/theme.ini'
}
inisection_map = {
    'classic_plugin': 'info',
    'classic_theme': 'theme',
    's_module': 'info',
    's_theme': 'info'
}

gh = addonregistry.GitHub()
db = addonregistry.Db()
releases_to_register = []
releases_to_remove = {}

# Set all registered releases to be removed from the database.
for r in db.releases():
    if r['addon_id'] not in releases_to_remove:
        releases_to_remove[r['addon_id']] = []
    releases_to_remove[r['addon_id']].append(r['release_id'])

# Compare each registered addon's releases/assets on GitHub against its
# registered releases.
for addon in db.addons():
    # Checking GitHub repository
    print 'Checking repository {}/{}:'.format(addon['owner'], addon['repo'])
    try:
        releases = gh.releases(addon['owner'], addon['repo'])
    except requests.exceptions.RequestException as e:
        # Repository not available; do not remove this repository's releases.
        # The repository could have been deleted, made private, or temporarily
        # unavailable. Here we err on the side of it being unavailable and leave
        # the releases alone.
        print '  Repository not available.'
        del releases_to_remove[addon['id']]
        continue

    if not releases:
        print '  Repository has no releases.'

    for release in releases:
        # Checking GitHub release
        print '  Checking release {} (tag={}):'.format(release['id'], release['tag_name'])

        if release['prerelease']:
            print '    Release is prerelease.'
            continue
        if release['draft']:
            print '    Release is a draft.'
            continue
        if not release['assets']:
            print '    Release has no asset.'
            continue

        asset = release['assets'][0] # Use first asset convention
        registered_release = db.release_is_registered(addon['id'], release['id'], asset['id'])
        if registered_release:
            # Release is already registered; do not remove this release
            print '    Release already registered (version={}).'.format(registered_release['version'])
            releases_to_remove[addon['id']].remove(release['id'])
            continue

        # Release is not registered; checking GitHub asset
        print '    Checking asset {}:'.format(asset['id'])
        if not asset['name'].lower().endswith('.zip'):
            # Asset does not have the .zip extension; do nothing
            print '      Asset does not have .zip extension.'
            continue

        try:
            response = requests.get(asset['browser_download_url'])
        except requests.exceptions.RequestException:
            # Asset not available; do nothing
            print '      Asset not available.'
            continue

        asset_filename = 'tmp/' + asset['name']
        with open(asset_filename, 'wb') as asset_file:
            asset_file.write(response.content)

        # Asset downloaded; checking ZIP file
        try:
            asset_zipfile = zipfile.ZipFile(asset_filename, 'r')
        except zipfile.BadZipfile:
            # Asset not a ZIP file; do nothing
            print '      Asset not a ZIP file.'
            continue

        # Asset is a ZIP file; checking ZIP file structure
        zip_dirs = [name for name in asset_zipfile.namelist() if name == addon['dirname'] + '/']
        if not zip_dirs:
            # The ZIP file must contain only one top-level directory, and that
            # directory must have the provided name; do nothing
            print '      Asset ZIP does not have valid top-level directory.'
            continue

        try:
            asset_inipath = addon['dirname'] + inipath_map[addon['type']]
            asset_inifile = asset_zipfile.open(asset_inipath)
        except KeyError:
            # INI file not found in archive; do nothing
            print '      INI file not found in ZIP.'
            continue

        try:
            parser = ConfigParser.ConfigParser()
            parser.readfp(asset_inifile)
        except ConfigParser.ParsingError:
            # INI formatted incorrectly (parsing error); do nothing
            print '      INI formatted incorrectly (parsing error).'
            continue

        try:
            ini = dict(parser.items(inisection_map[addon['type']]))
        except ConfigParser.NoSectionError:
            # INI formatted incorrectly (no [info] section); do nothing
            print '      INI formatted incorrectly (no [info] section).'
            continue

        if 'version' not in ini:
            # INI has no version; do nothing
            print '      INI has no version.'
            continue

        # Everything checks out; register release
        ini_version = ini['version'].strip('"')
        print '    Release is valid (version={}).'.format(ini_version)
        releases_to_register.append((
            addon['id'],
            release['id'],
            asset['id'],
            ini_version,
            asset['browser_download_url'],
            json.dumps(ini)
        ))

# Clean up.
print 'Cleaning up.'
[os.remove('tmp/' + f) for f in os.listdir('tmp') if f.lower().endswith('.zip')]

# Remove releases from the database. These are releases that are currently
# registered but do not meet criteria for registration anymore.
print 'Removing invalid releases.'
for addon_id, release_ids in releases_to_remove.iteritems():
    for release_id in release_ids:
        db.delete_release(addon_id, release_id)

# Add releases to the database. These are releases that are not currently
# registered and meet criteria for registration.
print 'Registering valid releases.'
for release_to_register in releases_to_register:
    try:
        db.insert_release(*release_to_register)
    except sqlite3.IntegrityError:
        # Addon version already exists; do nothing. This could only happen if a
        # repository has two or more unregistered releases that have identical
        # addon versions. This will only register the first, ignoring the rest.
        pass

# @todo: Build HTML files for each registered addon
