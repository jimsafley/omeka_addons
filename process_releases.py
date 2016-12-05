import ConfigParser
import json
import omekaaddons
import os
import requests
import sqlite3
import zipfile

inipath_map = {
    'classic_plugin': '/plugin.ini',
    'classic_theme': '/theme.ini',
    's_module': '/config/module.ini',
    's_theme': '/config/theme.ini'
}

gh = omekaaddons.GitHub()
db = omekaaddons.Db()
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
    try:
        releases = gh.releases(addon['owner'], addon['repo'])
    except requests.exceptions.RequestException as e:
        # Repository not available; do not remove this repository's releases
        del releases_to_remove[addon['id']]
        continue

    for release in releases:
        # Checking GitHub release
        if release['prerelease'] or release['draft'] or not release['assets']:
            # Release does not meet criteria for registration; do nothing
            continue

        # Release meets criteria for registration
        asset = release['assets'][0] # Use first asset convention
        if db.release_is_registered(addon['id'], release['id'], asset['id']):
            # Release is already registered; do not remove this release
            releases_to_remove[addon['id']].remove(release['id'])
            continue

        # Release is not registered; checking GitHub asset
        if not asset['name'].lower().endswith('.zip'):
            # Asset does not have the .zip extension; do nothing
            continue

        try:
            response = requests.get(asset['browser_download_url'])
        except requests.exceptions.RequestException:
            # Asset not available; do nothing
            continue

        asset_filename = 'tmp/' + asset['name']
        with open(asset_filename, 'wb') as asset_file:
            asset_file.write(response.content)

        # Asset downloaded; checking ZIP file
        try:
            asset_zipfile = zipfile.ZipFile(asset_filename, 'r')
        except zipfile.BadZipfile:
            # Asset not a ZIP file; do nothing
            continue

        # Asset is a ZIP file; checking ZIP file structure
        zip_dirs = [name for name in asset_zipfile.namelist() if name == addon['dirname'] + '/']
        if not zip_dirs:
            # The ZIP file must contain only one top-level directory, and that
            # directory must have the provided name; do nothing
            continue

        try:
            asset_inipath = addon['dirname'] + inipath_map[addon['type']]
            asset_inifile = asset_zipfile.open(asset_inipath)
        except KeyError:
            # INI file not found in archive; do nothing
            continue

        try:
            parser = ConfigParser.ConfigParser()
            parser.readfp(asset_inifile)
        except ConfigParser.ParsingError:
            # INI formatted incorrectly (parsing error); do nothing
            continue

        try:
            ini = dict(parser.items('info'))
        except ConfigParser.NoSectionError:
            # INI formatted incorrectly (no [info] section); do nothing
            continue

        if 'version' not in ini:
            # INI has no version; do nothing
            continue

        # Everything checks out; register release
        releases_to_register.append({
            'addon_id': addon['id'],
            'release_id': release['id'],
            'asset_id': asset['id'],
            'version': ini['version'].strip('"'),
            'download_url': asset['browser_download_url'],
            'ini': json.dumps(ini)
        })

# Clean up.
[os.remove('tmp/' + f) for f in os.listdir('tmp') if f.lower().endswith('.zip')]

# Remove releases from the database.
for addon_id, release_ids in releases_to_remove.iteritems():
    for release_id in release_ids:
        db.delete_release(addon_id, release_id)

# Add releases to the database.
for r in releases_to_register:
    try:
        db.insert_release(r['addon_id'], r['release_id'], r['asset_id'],
                          r['version'], r['download_url'], r['ini'])
    except sqlite3.IntegrityError:
        # Addon version already exists; do nothing. This could only happen if a
        # repository has two or more unregistered releases that have identical
        # addon versions. This will only register the first, ignoring the rest.
        pass

# @todo: Build HTML files for each addon in database
