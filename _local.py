import sqlite3

def db():
    """Get the local database object"""

    return Db()

class Db:
    conn = sqlite3.connect('addons.db')

    def insert_addon(self, owner, repo, type):
        with self.conn:
            sql = 'INSERT INTO addons (github_owner, github_repo, type) VALUES (?, ?, ?)'
            self.conn.execute(sql, (owner, repo, type))

    def addons(self):
        return self.conn.execute('SELECT * FROM addons')

    def create_db(self):
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS addons (
            id INTEGER PRIMARY KEY,
            github_owner TEXT,
            github_repo TEXT,
            type TEXT
        )''')
        self.conn.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS github_owner_repo
        ON addons(github_owner, github_repo)''')
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS releases (
            id INTEGER PRIMARY KEY,
            addon_id INTEGER
            github_release_id INTEGER,
            github_asset_id INTEGER,
            data TEXT,
            FOREIGN KEY(addon_id) REFERENCES addons(id)
        )''')

if __name__ == "__main__":
    db().create_db()
