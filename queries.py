import sqlite3


def add_object(con, name, box_id, available=1, date='NULL'):
    query = ('''
        INSERT INTO object (name, available, date, box_id)
        VALUES (?, ?, ?, ?)
        ''', (name, available, date, box_id))
    cur = con.cursor()
    cur.execute(query)
    cur.close()


def delete_object(con):
    pass


def edit_object(con):
    pass


def find_object_by_name(con):
    pass


def find_object_by_id(con):
    pass


def rent_object(con):
    pass


def return_object(con):
    pass


def history_object(con):
    pass


def add_room(con):
    pass


def remove_room(con):
    pass


def edit_room(con):
    pass


def add_restricted(con):
    pass


def remove_restricted(con):
    pass


def edit_restricted(con):
    pass
