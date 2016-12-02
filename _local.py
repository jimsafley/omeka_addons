import sqlite3

def db():
    return Db()

class Db:

    conn = sqlite3.connect('addons.db')
    conn.row_factory = sqlite3.Row

    def insert_addon(self, owner, repo, type, dirname):
        with self.conn:
            sql = 'INSERT INTO addons (owner, repo, type, dirname) VALUES (?, ?, ?, ?)'
            self.conn.execute(sql, (owner, repo, type, dirname))

    def addons(self):
        return self.conn.execute('SELECT * FROM addons')

    def release_is_registered(self, owner, repo, release_id, asset_id):
        sql = """
        SELECT *
        FROM addons
        JOIN releases ON addons.id = releases.addon_id
        WHERE addons.owner = ?
        AND addons.repo = ?
        AND releases.asset_id = ?
        AND releases.release_id = ?
        """
        return self.conn.execute(sql, (owner, repo, release_id, asset_id)).fetchone()

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

if __name__ == "__main__":
    db().create_db()
