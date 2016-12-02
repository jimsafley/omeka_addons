import _local
import _remote
import os
import json
import requests
import zipfile
from pprint import pprint

db = _local.db()
gh = _remote.gh()

# @todo: Create a releases_to_remove list containing all registered releases
# @todo: Create an empty releases_to_register list
releases_to_remove = []
releases_to_register = []

for addon in db.addons():
    # Checking repository
    try:
        releases = gh.releases(addon['owner'], addon['repo'])
    except requests.exceptions.RequestException as e:
        # Repository not available
        # @todo: Remove all this repository's releases from the releases_to_remove list
        pass
    else:
        for release in releases:
            # Checking release
            if release['prerelease'] or release['draft'] or not release['assets']:
                # Release does not meet criteria for registration; do nothing
                pass
            else:
                # Release meets criteria for registration
                asset = release['assets'][0] # Use first asset convention
                if db.release_is_registered(addon['owner'], addon['repo'], release['id'], asset['id']):
                    # Release is already registered
                    # @todo: Remove this release from the releases_to_remove list
                    pass
                else:
                    # Release is not registered; checking asset
                    asset_filename = 'tmp/' + asset['name']
                    asset_file = open(asset_filename, 'wb')
                    try:
                        response = requests.get(asset['browser_download_url'])
                    except requests.exceptions.RequestException:
                        # Asset not available; do nothing
                        pass
                    else:
                        asset_file.write(response.content)
                        asset_file.close()
                        # Asset downloaded; checking ZIP file
                        try:
                            asset_zipfile = zipfile.ZipFile(asset_filename, 'r')
                        except zipfile.BadZipfile:
                            # Asset not a ZIP file; do nothing
                            pass
                        else:
                            # Asset is a ZIP file; checking ZIP file structure
                            zip_dirs = [name for name in asset_zipfile.namelist() if name == addon['dirname'] + '/']
                            if not zip_dirs:
                                # The ZIP file must contain only one top-level
                                # directory, and that directory must have the
                                # provided name; do nothing
                                pass
                            else:
                                zip_ini = _local.get_ini(asset_zipfile, addon['type'], addon['dirname'])
                                if not zip_ini:
                                    # INI file not found or formatted incorrectly; do nothing
                                    pass
                                else:
                                    # Everything checks out; register release
                                    releases_to_register.append((
                                        addon['id'], release['id'], asset['id'],
                                        asset['browser_download_url'], json.dumps(zip_ini)
                                    ))
                            asset_zipfile.close()
                    os.remove(asset_filename)

# @todo: delete all downloaded files
# @todo: DELETE all releases in the releases_to_remove list
# @todo: INSERT all releases in the the releases_to_register list
# @todo: Build HTML files for each addon in database
pprint(releases_to_register)
