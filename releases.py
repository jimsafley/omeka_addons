import _local
import _remote
import pprint
import requests

db = _local.db()
gh = _remote.gh()

for addon in db.addons():
    print 'Checking repository {}/{}:'.format(addon['github_owner'], addon['github_repo'])
    try:
        releases = gh.releases(addon['github_owner'], addon['github_repo'])
    except requests.exceptions.HTTPError as e:
        print '  Repository not available.'
    except:
        # Unexpected error
        raise
    else:
        for release in releases:
            print '  Checking release {}:'.format(release['id'])
            if release['prerelease'] or release['draft'] or not release['assets']:
                print '    Release does not meet criteria for registration.'
            else:
                print '    Release meets criteria for registration:'
                asset = release.assets[0] # Use first asset convention
                if db.release_is_registered(addon['github_owner'], addon['github_repo'], release['id'], asset['id']):
                    print '      Release is already registered'
                else:
                    print '      Release is not registered'
