import sqlite3
import os


def connect_database(database):
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


def create(path, database):
    """
    Read a content in `path` and store it to `database`.
    `org_name` and `cur_name` will be the file name in `path`.
    """
    path = os.path.abspath(path)
    _, filename = os.path.split(path)

    con = connect_database(database)
    cur = con.cursor()
    with open(path) as f:
        # TODO: Hold the file path instead of file content for efficiency.
        cur.execute("""
            INSERT INTO files VALUES('{0}', '{0}', '{1}')
        """.format(filename, f.read()))
    con.commit()

    cur.close()
    con.close()


def retrieve(name, database):
    """
    Fetch the file content from `database` where the name is `name`.
    """
    con = connect_database(database)
    cur = con.cursor()
    res = cur.execute("""
        SELECT content FROM files WHERE cur_name='{0}'
    """.format(name))
    content = res.fetchone()
    assert content, "no such file exist on database, {0}".format(name)
    cur.close()
    con.close()
    return content[0]


def update(old_name, new_name, database):
    """
    Update the file name so that user can fetch the content with `new_name`
    """
    con = connect_database(database)
    cur = con.cursor()
    cur.execute("""
        UPDATE files SET cur_name='{1}' WHERE cur_name='{0}'
    """.format(old_name, new_name))
    con.commit()
    cur.close()
    con.close()


def delete(name, database):
    """
    Delete a file from database where the current name is `name`.
    """
    con = connect_database(database)
    cur = con.cursor()
    cur.execute("""
        DELETE FROM files WHERE cur_name='{0}'
    """.format(name))
    con.commit()
    cur.close()
    con.close()
