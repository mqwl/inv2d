import sqlite3


con = sqlite3.connect("inventory.db")
cur = con.cursor()


def init_db():
    # length, width and height are in cm
    query_initial_room = '''
    CREATE TABLE IF NOT EXISTS room(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        length INTEGER NOT NULL,
        width INTEGER NOT NULL,
        height INTEGER NOT NULL,
        CHECK (length > 0 AND width > 0 AND height > 0)
    );
    '''

    query_initial_restricted = '''
    CREATE TABLE IF NOT EXISTS restriction(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER NOT NULL,
        pivot_x INTEGER NOT NULL CHECK (pivot_x > 0),
        pivot_y INTEGER NOT NULL CHECK (pivot_y > 0),
        length INTEGER NOT NULL CHECK (length > 0),
        width INTEGER NOT NULL CHECK (width > 0),
        FOREIGN KEY (room_id) REFERENCES room (id)
    );
    '''

    query_initial_box = '''
    CREATE TABLE IF NOT EXISTS box(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        edge INTEGER NOT NULL CHECK (edge > 0),
        pivot_x INTEGER NOT NULL CHECK (pivot_x > 0),
        pivot_y INTEGER NOT NULL CHECK (pivot_y > 0),
        room_id INTEGER,
        FOREIGN KEY (room_id) REFERENCES room (id)
    );
    '''
    # available - boolean
    # date - ISO 8601 (YYYY-MM-DD)
    query_initial_object = '''
    CREATE TABLE IF NOT EXISTS object(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
                CHECK (length(name) >= 1 AND length(name) <= 500),
        available INTEGER NOT NULL DEFAULT 1,
        date TEXT DEFAULT NULL,
        box_id INTEGER,
        FOREIGN KEY (box_id) REFERENCES box (id)
    );
    '''

    cur.execute(query_initial_room)
    cur.execute(query_initial_restricted)
    cur.execute(query_initial_box)
    cur.execute(query_initial_object)


def print_db_info():
    # print every table name and its columns
    query_tablelist = '''
        SELECT name FROM sqlite_master
        WHERE type='table'
        ORDER BY name;
    '''
    cur.execute(query_tablelist)
    res = cur.fetchall()
    for row in res:
        print(row[0])
        cur.execute(f"PRAGMA table_info('{row[0]}');")
        columns = cur.fetchall()
        for col in columns:
            print(col)


def save_table():
    con.commit()


# save_table()
con.close()
