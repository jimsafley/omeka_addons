import argparse
import omekaaddons
import requests
import sqlite3
import sys

def register(owner, repo, type, dirname):
    gh = omekaaddons.GitHub()
    db = omekaaddons.Db()
    # Check that GitHub repository exists. Raises requests.exceptions.HTTPError if not.
    gh.repo(args.owner, args.repo)
    # Register Omeka addon. Raises sqlite3.IntegrityError if already registered.
    db.insert_addon(args.owner, args.repo, args.type, args.dirname)

if __name__ == '__main__':
    """Register an Omeka addon."""

    parser = argparse.ArgumentParser(description='Register a GitHub repository')
    parser.add_argument('--owner', required=True, help='The GitHub owner')
    parser.add_argument('--repo', required=True, help='The GitHub repository')
    parser.add_argument('--dirname', required=True, help='The Omeka addon directory name')
    parser.add_argument('--type', required=True, help='The Omeka addon type',
                        choices=['s_module', 's_theme', 'classic_plugin', 'classic_theme'])
    args = parser.parse_args()

    try:
        register(args.owner, args.repo, args.type, args.dirname)
    except requests.exceptions.HTTPError:
        sys.exit('GitHub repository not found')
    except sqlite3.IntegrityError:
        sys.exit('GitHub repository already registered')
    except:
        sys.exit('Unknown error')
