import sqlite3
import os


# Connect to specified database and create `files` table if it not exist.
# Returns `Connection` to `database`.
def connect_database(database):
    con = sqlite3.connect(database)
    cur = con.cursor()
    res = cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=files
    """)
    if len(res.fetchall()) == 0:
        cur.execute("CREATE TABLE files(org_name, cur_name, content)")
        con.commit()
    cur.close()
    return con


def create(path, database):
    _, filename = os.path.split(path)

    con = connect_database(database)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO files VALUES({0}, {0}, readfile({1}))
    """.format(filename, path))
    con.commit()

    cur.close()
    con.close()


def retrieve(name, database):
    con = connect_database(database)
    cur = con.cursor()
    res = cur.execute("""
        SELECT content FROM files WHERE cur_name={0}
    """.format(name))
    content = res.fetchone()
    cur.close()
    con.close()
    return content


def update(old_name, new_name, database):
    con = connect_database(database)
    cur = con.cursor()
    cur.execute("""
        UPDATE files SET cur_name={1} WHERE cur_name={0}
    """.format(old_name, new_name))
    cur.close()
    con.close()


def delete(name, database):
    con = connect_database(database)
    cur = con.cursor()
    cur.execute("""
        DELETE FROM files WHERE cur_name={0}
    """.format(name))
    cur.close()
    con.close()
