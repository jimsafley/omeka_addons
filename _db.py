import sqlite3

conn = sqlite3.connect('addons.db')

def create_db():
    conn.execute('''
    CREATE TABLE IF NOT EXISTS addons (
        id INTEGER PRIMARY KEY,
        github_owner TEXT,
        github_repo TEXT,
        type TEXT
    )''')
    conn.execute('''
    CREATE UNIQUE INDEX IF NOT EXISTS github_owner_repo
    ON addons(github_owner, github_repo)''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS releases (
        id INTEGER PRIMARY KEY,
        addon_id INTEGER
        github_release_id INTEGER,
        github_asset_id INTEGER,
        data TEXT,
        FOREIGN KEY(addon_id) REFERENCES addons(id)
    )''')

def insert_addon(owner, repo, type):
    with conn:
        conn.execute('INSERT INTO addons (github_owner, github_repo, type) VALUES (?, ?, ?)',
                     (owner, repo, type))

if __name__ == "__main__":
    create_db()
