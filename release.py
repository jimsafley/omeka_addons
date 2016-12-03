import argparse
import omekaaddons
import sqlite3
import sys

def register():
    pass

if __name__ == '__main__':
    """Register an Omeka addon release."""

    parser = argparse.ArgumentParser(description='Register a GitHub repository release')
    parser.add_argument('--owner', required=True, help='The GitHub owner')
    parser.add_argument('--repo', required=True, help='The GitHub repository')
    parser.add_argument('--release_id', required=True, help='The GitHub release ID')
    parser.add_argument('--asset_id', required=True, help='The GitHub asset ID')
    parser.add_argument('--version', required=True, help='The Omeka addon version for this release')
    parser.add_argument('--download_url', required=True, help='The GitHub asset download URL')
    parser.add_argument('--ini', required=True, help='The Omeka addon INI config for this release')
    args = parser.parse_args()
