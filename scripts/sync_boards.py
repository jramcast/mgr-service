#!/usr/bin/env python

import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONNECTION_STR = """
    user='{}'
    password='{}'
    dbname='{}'
    host='{}'
    port={}
""".format(
    os.environ['BOOKCORE_PGUSER'],
    os.environ['BOOKCORE_PGPASSWORD'],
    os.environ['BOOKCORE_PGDATABASE'],
    os.environ['BOOKCORE_PGHOST'],
    os.environ['BOOKCORE_PGPORT'],
)

SQL = """
    SELECT
        board.codigo,
        parent.codigo AS parent_board_code,
        board.nombre_es,
        board.nombre_en,
        board.nombre_ca,
        board.nombre_de,
        board.nombre_it,
        board.nombre_nl,
        board.nombre_fr,
        board.nombre_pt,
        board.nombre_ru,
        board.nombre_sv,
        board.nombre_ar,
        board.nombre_da,
        board.nombre_id,
        board.nombre_ja,
        board.nombre_ko,
        board.nombre_ms,
        board.nombre_no,
        board.nombre_th,
        board.nombre_tl,
        board.nombre_tr,
        board.nombre_vi,
        board.nombre_zh
    FROM reservas_pension board
        LEFT JOIN reservas_pension parent
            ON board.parent_board_id = parent.id
"""

OUTFILE_PATH = os.path.join(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
    ),
    "boards.json"
)

connection = psycopg2.connect(
    dsn=DB_CONNECTION_STR,
    cursor_factory=RealDictCursor
)

with connection.cursor() as cursor:
    cursor.execute(SQL)

    with open(OUTFILE_PATH, 'w') as outfile:
        json.dump(list(cursor), outfile)

print("Boards imported successfuly from bookcore to", OUTFILE_PATH)
