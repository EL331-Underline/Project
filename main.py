import sqlite3
import os


def connect_database(database: str | os.PathLike) -> sqlite3.Connection:
    """
    Connect to specified database and create `files` table if it not exist.
    Returns `Connection` to `database`.
    """
    con = sqlite3.connect(database)
    cur = con.cursor()
    res = cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name='files'
    """)
    if len(res.fetchall()) == 0:
        cur.execute("""
            CREATE TABLE files(org_name TEXT, cur_name TEXT, content TEXT)
        """)
        con.commit()
    cur.close()
    return con


class DatasetManager:
    """
    A simple dataset manager
    """

    def __init__(self, database: str | os.PathLike):
        self.con = connect_database(database)

    def __del__(self):
        self.con.close()

    def create(self, path: str | os.PathLike, name: str | None):
        """
        Read a content in `path` and store it to `database`.
        `org_name` and `cur_name` will be `name` if it isn't None.
        We use file name in `path` if `name` is None.
        """
        path = os.path.abspath(path)
        _, filename = os.path.split(path)
        assert len(filename) != 0, "no file name in path"
        if name is None:
            name = filename

        cur = self.con.cursor()
        with open(path) as f:
            # TODO: Hold the file path instead of file content for efficiency.
            cur.execute("""
                INSERT INTO files VALUES('{0}', '{0}', '{1}')
            """.format(name, f.read()))
            self.con.commit()
        cur.close()

    def retrieve(self, name: str):
        """
        Fetch the file content from `database` where the name is `name`.
        """
        cur = self.con.cursor()
        res = cur.execute("""
            SELECT content FROM files WHERE cur_name='{0}'
        """.format(name))
        content = res.fetchone()
        assert content, "no such file exist on database, {0}".format(name)
        cur.close()
        return content[0]

    def update(self, old_name: str, new_name: str):
        """
        Update the file name so that user can fetch the content with `new_name`
        """
        cur = self.con.cursor()
        cur.execute("""
            UPDATE files SET cur_name='{1}' WHERE cur_name='{0}'
        """.format(old_name, new_name))
        self.con.commit()
        cur.close()

    def delete(self, name: str):
        """
        Delete a file from database where the current name is `name`.
        """
        cur = self.con.cursor()
        cur.execute("""
            DELETE FROM files WHERE cur_name='{0}'
        """.format(name))
        self.con.commit()
        cur.close()
