import sqlite3


# TODO: add validation functions for everything,
#       implement rent history,
#       also possibly some extra functions...

def _run_query(con, query, values):
    cur = con.cursor()
    cur.execute(query, values)
    cur.close()


def add_box(con, edge, pivot_x, pivot_y, room_id):
    query = '''
        INSERT INTO box (edge, pivot_x, pivot_y, room_id)
        VALUES (?, ?, ?, ?)
        '''
    values = (edge, pivot_x, pivot_y, room_id)
    _run_query(con, query, values)


def remove_box(con, id):
    query = '''
        DELETE FROM box
        WHERE id = ?
        '''
    values = (id, )
    _run_query(con, query, values)


def edit_box(con, id, edge=-1, pivot_x=-1, pivot_y=-1, room_id=-1):
    to_update = {}
    if edge != -1:
        to_update['edge'] = edge
    if pivot_x != -1:
        to_update['pivot_x'] = pivot_x
    if pivot_y != -1:
        to_update['pivot_y'] = pivot_y
    if room_id != -1:
        to_update['room_id'] = room_id
    if not to_update:
        print('Nothing to update')
        return
    cols = ", ".join([f"{key} = ?" for key in to_update.keys()])
    to_update['id'] = id
    values = tuple(to_update.values())
    query = (f"UPDATE box SET {cols} WHERE id = ?")
    _run_query(con, query, values)


def print_box(con):
    query = 'SELECT * FROM box'
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    for res in results:
        print(res)
    cur.close()


def add_object(con, name, box_id, available=1, date='NULL'):
    query = '''
        INSERT INTO object (name, available, date, box_id)
        VALUES (?, ?, ?, ?)
        '''
    values = (name, available, date, box_id)
    _run_query(con, query, values)


def remove_object(con, id):
    query = '''
        DELETE FROM object
        WHERE id = ?
        '''
    values = (id, )
    _run_query(con, query, values)


def edit_object(con, id, name='', box_id=-1, available=-1, date=''):
    to_update = {}
    if name != '':
        to_update['name'] = name
    if box_id != -1:
        to_update['box_id'] = box_id
    if available != -1:
        to_update['available'] = available
    if date != '':
        to_update['date'] = date
    if not to_update:
        print('Nothing to update')
        return
    cols = ", ".join([f"{key} = ?" for key in to_update.keys()])
    to_update['id'] = id
    values = tuple(to_update.values())
    query = (f"UPDATE object SET {cols} WHERE id = ?")
    _run_query(con, query, values)


def find_object_by_name(con, name):
    query = '''
        SELECT * FROM object
        WHERE name = ?
        '''
    values = (name, )
    cur = con.cursor()
    cur.execute(query, values)
    results = cur.fetchall()
    for res in results:
        print(res)
    cur.close()


def find_object_by_id(con, id):
    query = '''
        SELECT * FROM object
        WHERE id = ?
        '''
    values = (id, )
    cur = con.cursor()
    cur.execute(query, values)
    results = cur.fetchall()
    for res in results:
        print(res)
    cur.close()


def rent_object(con, id, date):
    query = '''
        UPDATE object
        SET date = ?,
        available = 0
        WHERE id = ?
        '''
    values = (date, id)
    _run_query(con, query, values)


def return_object(con, id):
    query = '''
        UPDATE object
        SET date = 'NULL',
        available = 1
        WHERE id = ?
        '''
    values = (id, )
    _run_query(con, query, values)


# TODO: track renting of objects...
def history_object(con):
    pass


def print_object(con):
    query = 'SELECT * FROM object'
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    for res in results:
        print(res)
    cur.close()


def print_room(con):
    query = 'SELECT * FROM room'
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    for res in results:
        print(res)
    cur.close()


def add_room(con, name, length, width, height):
    query = '''
        INSERT INTO room (name, length, width, height)
        VALUES (?, ?, ?, ?)
        '''
    values = (name, length, width, height)
    _run_query(con, query, values)


def remove_room(con, id):
    query = '''
        DELETE FROM room
        WHERE id = ?
        '''
    values = (id, )
    _run_query(con, query, values)


def edit_room(con, id, name='', length=0, width=0, height=0):
    to_update = {}
    if name != '':
        to_update['name'] = name
    if length != 0:
        to_update['length'] = length
    if width != 0:
        to_update['width'] = width
    if height != 0:
        to_update['height'] = height
    if not to_update:
        print('Nothing to update')
        return
    cols = ", ".join([f"{key} = ?" for key in to_update.keys()])
    to_update['id'] = id
    values = tuple(to_update.values())
    query = (f"UPDATE room SET {cols} WHERE id = ?")
    _run_query(con, query, values)


def add_restricted(con, room_id, pivot_x, pivot_y, length, width):
    query = '''
        INSERT INTO restricted
        (room_id, pivot_x, pivot_y, length, width)
        VALUES (?, ?, ?, ?, ?)
        '''
    values = (room_id, pivot_x, pivot_y, length, width)
    _run_query(con, query, values)


def remove_restricted(con, id):
    query = '''
        DELETE FROM restricted
        WHERE id = ?
        '''
    values = (id, )
    _run_query(con, query, values)


def edit_restricted(con, id, room_id=-1, pivot_x=-1, pivot_y=-1, length=0, width=0):
    to_update = {}
    if room_id != -1:
        to_update['room_id'] = room_id
    if pivot_x != -1:
        to_update['length'] = length
    if pivot_y != -1:
        to_update['pivot_y'] = pivot_y
    if length != 0:
        to_update['length'] = length
    if width != 0:
        to_update['width'] = width
    if not to_update:
        print('Nothing to update')
        return
    cols = ", ".join([f"{key} = ?" for key in to_update.keys()])
    to_update['id'] = id
    values = tuple(to_update.values())
    query = (f"UPDATE restricted SET {cols} WHERE id = ?")
    _run_query(con, query, values)


def print_restricted(con):
    query = 'SELECT * FROM restricted'
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    for res in results:
        print(res)
    cur.close()
