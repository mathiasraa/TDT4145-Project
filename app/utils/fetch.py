import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def run_query(query):
    connection = sqlite3.connect("kaffedb.db")
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    connection.commit()
    connection.close()

    return rows
