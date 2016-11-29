import _db
import _github
import argparse
import requests
import sqlite3
import sys

parser = argparse.ArgumentParser(description='Register a GitHub repository')
parser.add_argument('--owner', required=True, help='The GitHub owner')
parser.add_argument('--repo', required=True, help='The GitHub repository')
parser.add_argument('--type', required=True, help='The type of Omeka addon',
                    choices=['s_module', 's_theme', 'classic_plugin', 'classic_theme'])
args = parser.parse_args()

try:
    repo = _github.repo(args.owner, args.repo)
except requests.exceptions.HTTPError:
    sys.exit('GitHub repository not found')

conn = sqlite3.connect('addons.db')
try:
    _db.insert_addon(args.owner, args.repo, args.type)
except sqlite3.IntegrityError:
    sys.exit('GitHub repository already registered')
