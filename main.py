import sqlite3
import os


def select(database):
    pass


def connect_database(database):
    con = sqlite3.connect(database)
    cur = con.cursor()
    res = cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name=files
    """)
    con.commit()
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
    pass


def update(old_name, new_name, database):
    pass


def delete(name, database):
    pass
