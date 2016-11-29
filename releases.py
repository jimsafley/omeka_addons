import logging
import pprint;
import sqlite3

logging.basicConfig(filename='errors.log', format='%(asctime)s %(levelname)s: %(message)s')
conn = sqlite3.connect('addons.db')

for addon in conn.execute('SELECT * FROM addons'):
    pprint.pprint(addon)

#~ for addon in addons:
    #~ releases = api.releases(addon['github_owner'], addon['github_repo'])
    #~ if releases is False:
        #~ # Error thrown during API request. Do nothing.
        #~ pass
    #~ else:
        #~ for release in releases:
            #~ # Do not process draft releases, pre-releases, or releases without
            #~ # at least one asset.
            #~ if not release['prerelease'] and not release['draft'] and release['assets']:
                #~ asset = release['assets'][0] # use first asset convention
                #~ # We know about a release if the stored release/asset IDs and
                #~ # the remote release/asset IDs match.
                #~ if release['id'] in addon['releases'] and asset['id'] == addon['releases'][release['id']]['github_asset_id']:
                    #~ # We know about this release.
                    #~ pass
                #~ else:
                    #~ # We don't know about this release.
                    #~ pass

