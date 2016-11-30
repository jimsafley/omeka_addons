import _local
import _remote
import argparse
import sqlite3
import sys

parser = argparse.ArgumentParser(description='Register a GitHub repository')
parser.add_argument('--owner', required=True, help='The GitHub owner')
parser.add_argument('--repo', required=True, help='The GitHub repository')
parser.add_argument('--type', required=True, help='The type of Omeka addon',
                    choices=['s_module', 's_theme', 'classic_plugin', 'classic_theme'])
args = parser.parse_args()

repo = _remote.gh().repository(args.owner, args.repo)
if (not repo):
    sys.exit('GitHub repository not found')

try:
    _local.db().insert_addon(args.owner, args.repo, args.type)
except sqlite3.IntegrityError:
    sys.exit('GitHub repository already registered')
