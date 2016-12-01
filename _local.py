import sqlite3
import pprint

def db():
    return Db()

class Db:

    conn = sqlite3.connect('addons.db')
    conn.row_factory = sqlite3.Row

    def insert_addon(self, owner, repo, type):
        with self.conn:
            sql = 'INSERT INTO addons (github_owner, github_repo, type) VALUES (?, ?, ?)'
            self.conn.execute(sql, (owner, repo, type))

    def addons(self):
        return self.conn.execute('SELECT * FROM addons')

    def release_is_registered(self, owner, repo, release_id, asset_id):
        sql = """
        SELECT *
        FROM addons
        JOIN releases ON addons.id = releases.addon_id
        WHERE addons.github_owner = ?
        AND addons.github_repo = ?
        AND releases.github_asset_id = ?
        AND releases.github_release_id = ?
        """
        return self.conn.execute(sql, (owner, repo, release_id, asset_id)).fetchone()

    def create_db(self):
        c = self.conn.cursor()
        c.executescript("""
        CREATE TABLE IF NOT EXISTS addons (
            id INTEGER PRIMARY KEY,
            github_owner TEXT,
            github_repo TEXT,
            type TEXT
        );

        CREATE UNIQUE INDEX IF NOT EXISTS github_owner_repo
        ON addons(github_owner, github_repo);

        CREATE TABLE IF NOT EXISTS releases (
            id INTEGER PRIMARY KEY,
            addon_id INTEGER,
            github_release_id INTEGER,
            github_asset_id INTEGER,
            data TEXT,
            FOREIGN KEY(addon_id) REFERENCES addons(id)
        );
        """)

if __name__ == "__main__":
    db().create_db()
