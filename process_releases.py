import ConfigParser
import json
import omekaaddons
import os
from pprint import pprint
import requests
import zipfile

gh = omekaaddons.GitHub()
db = omekaaddons.Db()
inipath_map = {
    'classic_plugin': '/plugin.ini',
    'classic_theme': '/theme.ini',
    's_module': '/config/module.ini',
    's_theme': '/config/theme.ini'
}

# @todo: Create a releases_to_remove list containing all registered releases
# @todo: Create an empty releases_to_register list
releases_to_remove = [] # {addon_id: [release_id, release_id]}
releases_to_register = []

for addon in db.addons():
    # Checking repository
    try:
        releases = gh.releases(addon['owner'], addon['repo'])
    except requests.exceptions.RequestException as e:
        # Repository not available
        # @todo: Remove all this repository's releases from the releases_to_remove list
        continue

    for release in releases:
        # Checking release
        if release['prerelease'] or release['draft'] or not release['assets']:
            # Release does not meet criteria for registration; do nothing
            continue

        # Release meets criteria for registration
        asset = release['assets'][0] # Use first asset convention
        if db.release_is_registered(addon['id'], release['id'], asset['id']):
            # Release is already registered
            # @todo: Remove this release from the releases_to_remove list
            continue

        # Release is not registered; checking asset
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
            # The ZIP file must contain only one top-level directory, and that directory must have the provided name; do nothing
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
        releases_to_register.append((
            addon['id'], release['id'], asset['id'],
            ini['version'].strip('"'),
            asset['browser_download_url'],
            json.dumps(ini)
        ))

# Clean up.
[os.remove('tmp/' + f) for f in os.listdir('tmp') if f.lower().endswith('.zip')]

# @todo: DELETE all releases in the releases_to_remove list
# @todo: INSERT all releases in the the releases_to_register list
# @todo: Build HTML files for each addon in database
pprint(releases_to_register)
