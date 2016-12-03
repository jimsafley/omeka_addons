import requests
from requests.utils import quote
import sqlite3

class GitHub:
    """Access the GitHub API"""

    client_id = 'aad23add2728eddf4da3'
    client_secret = '4f44af7870b0dc62bac752d82a1ca52547d360fd'

    def _request(self, endpoint):
        params = {'client_id': self.client_id, 'client_secret': self.client_secret}
        response = requests.get('https://api.github.com' + endpoint, params=params)
        response.raise_for_status()
        return response.json()

    def repo(self, owner, repo):
        endpoint = '/repos/{}/{}'.format(quote(owner), quote(repo))
        return self._request(endpoint)

    def releases(self, owner, repo):
        endpoint = '/repos/{}/{}/releases'.format(quote(owner), quote(repo))
        return self._request(endpoint)

class Db:
    """Access the addons database"""

    conn = sqlite3.connect('omekaaddons.db')
    conn.row_factory = sqlite3.Row

    def insert_addon(self, owner, repo, type, dirname):
        with self.conn:
            sql = 'INSERT INTO addons (owner, repo, type, dirname) VALUES (?, ?, ?, ?)'
            self.conn.execute(sql, (owner, repo, type, dirname))

    def addons(self):
        return self.conn.execute('SELECT * FROM addons')

    def releases(self):
        return self.conn.execute('SELECT * FROM releases')

    def release_is_registered(self, addon_id, release_id, asset_id):
        sql = """
        SELECT *
        FROM releases
        WHERE addon_id = ?
        AND asset_id = ?
        AND release_id = ?
        """
        return self.conn.execute(sql, (asset_id, release_id, asset_id)).fetchone()

    def create_db(self):
        c = self.conn.cursor()
        c.executescript("""
        CREATE TABLE IF NOT EXISTS addons (
            id INTEGER PRIMARY KEY,
            owner TEXT,
            repo TEXT,
            type TEXT,
            dirname TEXT
        );
        CREATE UNIQUE INDEX IF NOT EXISTS owner_repo
        ON addons(owner, repo);
        CREATE UNIQUE INDEX IF NOT EXISTS dirname_type
        ON addons(dirname, type);
        CREATE TABLE IF NOT EXISTS releases (
            id INTEGER PRIMARY KEY,
            addon_id INTEGER,
            release_id INTEGER,
            asset_id INTEGER,
            version TEXT,
            download_url TEXT,
            ini TEXT,
            FOREIGN KEY(addon_id) REFERENCES addons(id)
        );
        CREATE UNIQUE INDEX IF NOT EXISTS addon_version
        ON releases(addon_id, version);
        """)
