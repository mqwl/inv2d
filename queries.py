import sqlite3
import ezdxf
from datetime import date as dt
from ezdxf.addons import binpacking as bp
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf import colors
from typing import List
import matplotlib.pyplot as plt
from ezdxf.math import Matrix44
import numpy as np
import io
from PIL import Image

# TODO: add validation,
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
    check_query = ('''
        SELECT length, width, height
        FROM room
        WHERE id = ?
        ''')
    values2 = (room_id, )
    cur = con.cursor()
    cur.execute(check_query, values2)
    check_result = cur.fetchone()
    cur.close()
    permitted = True
    for res in check_result:
        if edge > res:
            permitted = False
    if permitted:
        _run_query(con, query, values)
    else:
        print('Коробка слишком большая')


def remove_box(con, id):
    query = '''
        DELETE FROM box
        WHERE id = ?
        '''
    values = (id, )
    _run_query(con, query, values)


def edit_box(con, id, edge=-1, pivot_x=-1, pivot_y=-1, room_id=-1):
    to_update = {}
    room_cur_id = room_id
    if edge != -1:
        to_update['edge'] = edge
    if pivot_x != -1:
        to_update['pivot_x'] = pivot_x
    if pivot_y != -1:
        to_update['pivot_y'] = pivot_y
    if room_id != -1:
        to_update['room_id'] = room_id
    else:
        room_query = ('''
            SELECT room_id
            FROM box
            WHERE id = ?
            ''')
        room_val = (id, )
        cur_room = con.cursor()
        cur_room.execute(room_query, room_val)
        room_cur_id = cur_room.fetchone()[0]
        cur_room.close()
    if not to_update:
        print('Nothing to update')
        return
    cols = ", ".join([f"{key} = ?" for key in to_update.keys()])
    to_update['id'] = id
    values = tuple(to_update.values())
    query = (f"UPDATE box SET {cols} WHERE id = ?")
    check_query = ('''
        SELECT length, width, height
        FROM room
        WHERE id = ?
        ''')
    values2 = (room_cur_id, )
    cur = con.cursor()
    cur.execute(check_query, values2)
    check_result = cur.fetchone()
    cur.close()
    permitted = True
    for res in check_result:
        if edge > res:
            permitted = False
    if permitted:
        _run_query(con, query, values)
    else:
        print('Коробка слишком большая')


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
    query_object = '''
        UPDATE object
        SET date = ?,
        available = 0
        WHERE id = ?
        '''
    values_o = (date, id)
    query_movement = '''
        INSERT INTO movement (object_id, date_rent, date_return)
        VALUES (?, ?, ?)
        '''
    today = dt.today().strftime("%Y-%m-%d")
    values_m = (id, today, date)
    try:
        _run_query(con, query_object, values_o)
        _run_query(con, query_movement, values_m)
    except Exception as e:
        print(f'Error: {e}')


def return_object(con, obj_id, rent_id):
    query_object = '''
        UPDATE object
        SET date = 'NULL',
        available = 1
        WHERE id = ?
        '''
    values_o = (obj_id, )
    query_movement = '''
        UPDATE movement
        SET finished = 1
        WHERE id = ?
        '''
    values_m = (rent_id, )
    try:
        _run_query(con, query_object, values_o)
        _run_query(con, query_movement, values_m)
    except Exception as e:
        print(f'Error: {e}')


# all movements of an object
def history_object(con, id):
    query = '''
        SELECT * FROM movement
        WHERE object_id = ?
        '''
    values = (id, )
    cur = con.cursor()
    cur.execute(query, values)
    results = cur.fetchall()
    for res in results:
        print(res)
    cur.close()


def print_movement(con):
    query = 'SELECT * FROM movement'
    cur = con.cursor()
    cur.execute(query)
    results = cur.fetchall()
    for res in results:
        print(res)
    cur.close()


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


def make_doc():
    doc = ezdxf.new()
    doc.layers.add("FRAME", color=colors.YELLOW)
    doc.layers.add("ITEMS")
    doc.layers.add("TEXT")
    return doc


def setup_iso_view(doc, model_size=(1000, 1000, 1000)):
    layout = doc.layout('Layout1')
    layout.page_setup(size=(297, 210), units='mm')
    cx = model_size[0] / 2
    cy = model_size[1] / 2
    v_height = max(model_size) * 1.5
    vport = layout.add_viewport(
        center=(148, 105),
        size=(280, 190),
        view_center_point=(cx, cy),
        view_height=v_height
    )
    vport.dxf.view_direction_vector = (1, -1, 1)
    vport.dxf.status = 1
    vport.dxf.flags = 1
    doc.header['$EXTMIN'] = (0, 0, 0)
    doc.header['$EXTMAX'] = model_size


def render_placement(doc):
    ctx = RenderContext(doc)
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_axes([0, 0, 1, 1])
    out = MatplotlibBackend(ax)
    frontend = Frontend(ctx, out)
    m = Matrix44.chain(
        Matrix44.z_rotate(np.radians(45)),
        Matrix44.x_rotate(np.radians(-55))  # угол ракурса
    )
    msp = doc.modelspace()
    transformed_entities = []
    for entity in msp:
        try:
            copy = entity.copy()
            copy.transform(m)
            transformed_entities.append(copy)
        except Exception:
            continue
    if transformed_entities:
        frontend.draw_entities(transformed_entities)
    ax.autoscale()
    ax.set_aspect('equal')
    ax.axis('off')
    # ---------------
    # Экспорт в PNG:
    # fig.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)


def calculate_placement(con, id):
    # размеры искомой комнаты
    cur2 = con.cursor()
    values = (id, )
    query2 = 'SELECT name, width, height, length FROM room WHERE id = ?'
    cur2.execute(query2, values)
    results2 = cur2.fetchone()
    print(results2)
    bin = (results2[0], results2[3], results2[1], results2[2])
    packer = bp.Packer()
    packer.add_bin(*bin)
    # коробки из искомой комнаты
    query = 'SELECT id, edge FROM box WHERE room_id = ?'
    cur = con.cursor()
    cur.execute(query, values)
    results = cur.fetchall()
    cur.close()
    bins: List[bp.Bin] = []
    # добавляем коробки в комнату
    for res in results:
        box_id = res[0]
        size = float(res[1])
        print(f"Пытаюсь добавить коробку размером: {size}")
        packer.add_item(box_id, size, size, size)
    cur2.close()
    packer.pack(bp.PickStrategy.BIGGER_FIRST)
    bins.extend(packer.bins)
    cur3 = con.cursor()
    for bin in packer.bins:
        for item in bin.items:
            x, y, z = item.position
            cur3.execute('''
                UPDATE box
                SET pivot_x = ?, pivot_y = ?
                WHERE id = ?
            ''', (x, y, item.payload))
    con.commit()
    cur3.close()
    doc = make_doc()
    msp = doc.modelspace()
    bp.export_dxf(msp, bins, offset=(0, 0, 0))
    room_size = (results2[1], results2[2], results2[3])
    setup_iso_view(doc, model_size=room_size)

    return render_placement(doc)
