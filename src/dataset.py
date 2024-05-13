import sqlite3
import os
import unittest


def connect_database(database: str | os.PathLike) -> sqlite3.Connection:
    """
    Connect to specified database and create `files` table if it not exist.
    Returns `Connection` to `database`.

    `files` has three columns:
    - `org_name` is original name of the file
    - `cur_name` is updated name of the file
    - `path` is the absolute path of the file
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
            CREATE TABLE files(org_name TEXT, cur_name TEXT, path TEXT)
        """)
        con.commit()
    cur.close()
    return con


class TestConnectDatabase(unittest.TestCase):
    def test_connect_database(self):
        pass


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
        Store the path with `org_name` and `cur_name` is `name`.
        If `name` is None, use file name in `path` instead.
        """
        path = os.path.abspath(path)
        _, filename = os.path.split(path)
        assert len(filename) != 0, "no file name in path"
        if name is None:
            name = filename

        cur = self.con.cursor()
        cur.execute("""
            INSERT INTO files VALUES('{0}', '{0}', '{1}')
        """.format(name, path))
        self.con.commit()
        cur.close()

    def retrieve(self, name: str) -> str:
        """
        Fetch the file content from `database` where the name is `name`.
        """
        cur = self.con.cursor()
        res = cur.execute("""
            SELECT path FROM files WHERE cur_name='{0}'
        """.format(name))
        path = res.fetchone()
        assert path, "no such file exist on database, {0}".format(name)
        cur.close()

        with open(path[0]) as f:
            return f.read()

    def retrieve_names(self) -> list[str]:
        """
        Fetch all names in database.
        """
        cur = self.con.cursor()
        res = cur.execute("""
            SELECT cur_name FROM files
        """)
        names = []
        for name in res.fetchall():
            names.append(name[0])
        return names

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


class TestDatasetManager(unittest.TestCase):
    def test_create(self):
        pass

    def test_retrieve(self):
        pass

    def test_retrieve_names(self):
        pass

    def test_update(self):
        pass

    def test_delete(self):
        pass


if __name__ == "__main__":
    unittest.main()
