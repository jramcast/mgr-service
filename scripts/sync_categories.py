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

REMOVABLE_COLUMNS = [
    "nombre_corto_es",
    "nombre_corto_en",
    "nombre_corto_ca",
    "nombre_corto_de",
    "nombre_corto_it",
    "nombre_corto_nl",
    "nombre_corto_fr",
    "nombre_corto_pt",
    "nombre_corto_ru",
    "nombre_corto_sv",
    "nombre_corto_ar",
    "nombre_corto_da",
    "nombre_corto_id",
    "nombre_corto_ja",
    "nombre_corto_ko",
    "nombre_corto_ms",
    "nombre_corto_no",
    "nombre_corto_th",
    "nombre_corto_tl",
    "nombre_corto_tr",
    "nombre_corto_vi",
    "nombre_corto_zh"
]

SQL = """
    SELECT
        codigo,
        nombre_es,
        nombre_en,
        nombre_ca,
        nombre_de,
        nombre_it,
        nombre_nl,
        nombre_fr,
        nombre_pt,
        nombre_ru,
        nombre_sv,
        nombre_ar,
        nombre_da,
        nombre_id,
        nombre_ja,
        nombre_ko,
        nombre_ms,
        nombre_no,
        nombre_th,
        nombre_tl,
        nombre_tr,
        nombre_vi,
        nombre_zh,
        {}
    FROM hotel_categoria
""".format(','.join(REMOVABLE_COLUMNS))

OUTFILE_PATH = os.path.join(
    os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
    ),
    "categories.json"
)

connection = psycopg2.connect(
    dsn=DB_CONNECTION_STR,
    cursor_factory=RealDictCursor
)

with connection.cursor() as cursor:
    cursor.execute(SQL)
    data = list(cursor)

for category in data:
    for key, value in category.items():
        if "nombre_corto_" in key:
            normalized_key = key.replace("_corto", '')
            if not category.get(normalized_key):
                category[normalized_key] = value

    for key in REMOVABLE_COLUMNS:
        del category[key]

with open(OUTFILE_PATH, 'w') as outfile:
    json.dump(data, outfile)

print("Categories imported successfuly from bookcore to", OUTFILE_PATH)
