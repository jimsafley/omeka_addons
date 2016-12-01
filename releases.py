import _local
import _remote
import requests
import zipfile
from pprint import pprint

db = _local.db()
gh = _remote.gh()

# @todo: Create a releases-to-be-removed list containing all registered releases
# @todo: Create an empty releases-to-be-registered list

for addon in db.addons():
    # Checking repository
    try:
        releases = gh.releases(addon['owner'], addon['repo'])
    except requests.exceptions.RequestException as e:
        # Repository not available
        # @todo: Remove all this repository's releases from the releases-to-be-removed list
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
                    # @todo: Remove this release from the releases-to-be-removed list
                    pass
                else:
                    # Release is not registered; checking asset
                    asset_filename = asset['name']
                    asset_file = open(asset_filename, 'wb')
                    try:
                        response = requests.get(asset['browser_download_url'])
                    except requests.exceptions.RequestException:
                        # Asset file not available; do nothing
                        pass
                    else:
                        asset_file.write(response.content)
                        asset_file.close()
                        # Asset file downloaded; checking ZIP
                        try:
                            asset_zipfile = zipfile.ZipFile(asset_filename, 'r')
                        except zipfile.BadZipfile:
                            # Asset file is not a ZIP file; do nothing
                            pass
                        else:
                            # Asset file is a ZIP file; checking structure
                            zip_dirs = [name for name in asset_zipfile.namelist() if name == addon['dirname'] + '/']
                            if not zip_dirs:
                                # Asset zip file does not contain one top-level
                                # directory with the provided name; do nothing
                                pass
                            else:
                                zip_ini = _local.get_ini(asset_zipfile, addon['type'], addon['dirname'])
                                pprint(asset)

                    # @todo: Download asset, checking that it's a valid addon for Omeka type
                    # @todo: If not valid: do nothing
                    # @todo: If valid: add this release to the releases-to-be-registered list

# @todo: DELETE all releases in the releases-to-be-removed list
# @todo: INSERT all releases in the the releases-to-be-registered list
# @todo: Build HTML files for each addon in database
