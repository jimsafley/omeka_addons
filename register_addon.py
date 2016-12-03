import argparse
import omekaaddons
import sqlite3
import sys

parser = argparse.ArgumentParser(description='Register a GitHub repository')
parser.add_argument('--owner', required=True, help='The GitHub owner')
parser.add_argument('--repo', required=True, help='The GitHub repository')
parser.add_argument('--dirname', required=True, help='The Omeka addon directory name')
parser.add_argument('--type', required=True, help='The Omeka addon type',
                    choices=['s_module', 's_theme', 'classic_plugin', 'classic_theme'])
args = parser.parse_args()

gh = omekaaddons.GitHub()
db = omekaaddons.Db()

repo = gh.repo(args.owner, args.repo)
if not repo:
    sys.exit('GitHub repository not found')

try:
    db.insert_addon(args.owner, args.repo, args.type, args.dirname)
except sqlite3.IntegrityError:
    sys.exit('GitHub repository already registered')
