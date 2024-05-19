import sqlite3
import os
import unittest
from tempfile import NamedTemporaryFile


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
    def test_connect_database_with_empty_db(self):
        with NamedTemporaryFile(suffix="db") as db:
            con = connect_database(db.name)

            cur = con.cursor()
            res = cur.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type='table' AND name='files'
            """)
            names = res.fetchall()
            cur.close()
            assert len(names) == 1

            # Check `connect_database` creates empty `files`
            cur = con.cursor()
            res = cur.execute("""
                SELECT * FROM files
            """)
            files = res.fetchall()
            cur.close()
            assert len(files) == 0

    def test_connect_database_with_non_empty_db(self):
        with NamedTemporaryFile(suffix="db") as db:
            # Create `files` table and insert a value.
            con = sqlite3.connect(db.name)
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE files(org_name TEXT, cur_name TEXT, path TEXT)
            """)
            con.commit()
            cur.execute("""
                INSERT INTO files VALUES('test org', 'test cur', 'test path')
            """)
            con.commit()
            cur.close()
            con.close()

            con = connect_database(db.name)

            # Check if `files` table is not modified by `connect_database`.
            cur = con.cursor()
            res = cur.execute("""
                SELECT * FROM files
            """)
            files = res.fetchall()
            cur.close()
            assert len(files) == 1
            assert ("test org", "test cur", "test path") in files


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
        with NamedTemporaryFile(suffix="db") as db, \
                NamedTemporaryFile() as f1, \
                NamedTemporaryFile() as f2:
            m = DatasetManager(db.name)
            m.create(f1.name, None)
            m.create(f2.name, "f2-alias")

            cur = m.con.cursor()
            res = cur.execute("""
                SELECT * FROM files
            """)
            files = res.fetchall()
            cur.close()

            f1_name = os.path.split(f1.name)[1]
            f2_name = "f2-alias"
            assert len(files) == 2
            assert (f1_name, f1_name, f1.name) in files
            assert (f2_name, f2_name, f2.name) in files

    def test_retrieve(self):
        with NamedTemporaryFile(suffix="db") as db, NamedTemporaryFile() as f:
            m = DatasetManager(db.name)
            m.create(f.name, "file")

            with open(f.name, "w") as f:
                f.write("test sentence")
            fetched = m.retrieve("file")
            assert fetched == "test sentence", fetched

    def test_retrieve_names(self):
        with NamedTemporaryFile(suffix="db") as db, \
                NamedTemporaryFile() as f1, \
                NamedTemporaryFile() as f2:
            m = DatasetManager(db.name)
            m.create(f1.name, "file1")
            m.create(f2.name, "file2")
            names = m.retrieve_names()
            assert len(names) == 2
            assert "file1" in names
            assert "file2" in names

    def test_update(self):
        with NamedTemporaryFile(suffix="db") as db, NamedTemporaryFile() as f1:
            m = DatasetManager(db.name)
            m.create(f1.name, "file1")

            m.update("file1", "new file1")

            cur = m.con.cursor()
            res = cur.execute("""
                SELECT org_name, cur_name FROM files
            """)
            names = res.fetchall()
            cur.close()
            assert len(names) == 1
            assert ("file1", "new file1") in names

    def test_delete(self):
        with NamedTemporaryFile(suffix="db") as db, NamedTemporaryFile() as f1:
            m = DatasetManager(db.name)
            m.create(f1.name, "file1")

            cur = m.con.cursor()
            res = cur.execute("""
                SELECT * FROM files
            """)
            files = res.fetchall()
            cur.close()
            assert len(files) == 1
            assert ("file1", "file1", f1.name) in files

            m.delete("file1")

            cur = m.con.cursor()
            res = cur.execute("""
                SELECT * FROM files
            """)
            files = res.fetchall()
            cur.close()
            assert len(files) == 0


if __name__ == "__main__":
    unittest.main()
