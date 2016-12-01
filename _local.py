import ConfigParser
import StringIO
import sqlite3

def db():
    return Db()

def get_ini(zipfile, type, dirname):
    ini_header = ''
    if type == 'classic_plugin':
        ini_path = '/plugin.ini'
    elif type == 'classic_theme':
        ini_path = '/theme.ini'
    elif type == 's_module':
        ini_header = '[info]\n'
        ini_path = '/config/module.ini'
    elif type == 's_theme':
        ini_header = '[info]\n'
        ini_path = '/config/theme.ini'

    try:
        ini = zipfile.read(dirname + ini_path)
    except KeyError:
        # INI file not found in archive
        return False

    # ConfigParser requires INI section headers.
    ini_buffer = StringIO.StringIO(ini_header + ini)
    parser = ConfigParser.ConfigParser()

    try:
        parser.readfp(ini_buffer)
    except ConfigParser.ParsingError:
        # INI formatted incorrectly (parsing error)
        return False

    try:
        return parser.items('info')
    except ConfigParser.NoSectionError:
        # INI formatted incorrectly (no [info] section)
        return False

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
            data TEXT,
            FOREIGN KEY(addon_id) REFERENCES addons(id)
        );
        """)

if __name__ == "__main__":
    db().create_db()
