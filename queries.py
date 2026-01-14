import sqlite3


# TODO: add validation functions for everything,
#       implement rent history,
#       also possibly some extra functions...

def _run_query(con, query):
    cur = con.cursor()
    cur.execute(query)
    cur.close()


def add_object(con, name, box_id, available=1, date='NULL'):
    query = ('''
        INSERT INTO object (name, available, date, box_id)
        VALUES (?, ?, ?, ?)
        ''', (name, available, date, box_id))
    _run_query(con, query)


def delete_object(con, id):
    query = ('''
        DELETE FROM object
        WHERE id = ?
        ''', (id))
    _run_query(con, query)


def edit_object(con, id, name='', box_id=-1, available=-1, date=''):
    to_update = {}
    if name != '':
        to_update[name] = name
    if box_id != -1:
        to_update[box_id] = box_id
    if available != -1:
        to_update[available] = available
    if date != '':
        to_update[date] = date
    if not to_update:
        print('Nothing to update')
        return
    to_update[id] = id
    cols = ", ".join([f"{key} = ?" for key in to_update.keys()])
    values = list(to_update.values())
    query = (f"UPDATE object SET {cols} WHERE id = ?")
    cur = con.cursor()
    cur.execute(query, values)
    cur.close()


def find_object_by_name(con, name):
    query = ('''
        SELECT * FROM object
        WHERE name = ?
        ''', (name))
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    for res in results:
        print(res)
    cur.close()


def find_object_by_id(con, id):
    query = ('''
        SELECT * FROM object
        WHERE id = ?
        ''', (id))
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    for res in results:
        print(res)
    cur.close()


def rent_object(con, id, date):
    query = ('''
        UPDATE object
        SET date = ?,
        available = 0
        WHERE id = ?
        ''', (date, id))
    _run_query(con, query)


def return_object(con, id):
    query = ('''
        UPDATE object
        SET date = NULL,
        available = 1
        WHERE id = ?
        ''', (id))
    _run_query(con, query)


# TODO: track renting of objects...
def history_object(con):
    pass


def add_room(con, length, width, height):
    query = ('''
        INSERT INTO room (length, width, height)
        VALUES (?, ?, ?)
        ''', (length, width, height))
    _run_query(con, query)


def remove_room(con, id):
    query = ('''
        DELETE FROM room
        WHERE id = ?
        ''', (id))
    _run_query(con, query)


def edit_room(con, id, length=0, width=0, height=0):
    to_update = {}
    if length != 0:
        to_update[length] = length
    if width != 0:
        to_update[width] = width
    if height != 0:
        to_update[height] = height
    if not to_update:
        print('Nothing to update')
        return
    to_update[id] = id
    cols = ", ".join([f"{key} = ?" for key in to_update.keys()])
    values = list(to_update.values())
    query = (f"UPDATE room SET {cols} WHERE id = ?")
    cur = con.cursor()
    cur.execute(query, values)
    cur.close()


def add_restricted(con, room_id, pivot_x, pivot_y, length, width):
    query = ('''
        INSERT INTO restricted
        (room_id, pivot_x, pivot_y, length, width)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (room_id, pivot_x, pivot_y, length, width))
    _run_query(con, query)


def remove_restricted(con, id):
    query = ('''
        DELETE FROM restricted
        WHERE id = ?
        ''', (id))
    _run_query(con, query)


def edit_restricted(con, id, room_id=-1, pivot_x=-1, pivot_y=-1, length=0, width=0):
    to_update = {}
    if room_id != -1:
        to_update[room_id] = room_id
    if pivot_x != -1:
        to_update[length] = length
    if pivot_y != -1:
        to_update[pivot_y] = pivot_y
    if length != 0:
        to_update[length] = length
    if width != 0:
        to_update[width] = width
    if not to_update:
        print('Nothing to update')
        return
    to_update[id] = id
    cols = ", ".join([f"{key} = ?" for key in to_update.keys()])
    values = list(to_update.values())
    query = (f"UPDATE restricted SET {cols} WHERE id = ?")
    cur = con.cursor()
    cur.execute(query, values)
    cur.close()
