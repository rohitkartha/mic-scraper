from typing import Union
import sqlite3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    conn  = sqlite3.connect('us_mic_data.db')

    cursor = conn.cursor()

    cur = cursor.execute('''
        SELECT * FROM shows
    ''')

    rows = cur.fetchall()
    
    shows = []
    for row in rows:
        show = {
            'show_id': row[0],
            'state_name': row[1],
            'city_name': row[2],
            'show_name': row[3],
            'show_date': row[4],
            'show_time': row[5],
            'show_venue': row[6],
            'show_address': row[7],
            'show_freq': row[8],
            'show_cost': row[9],
            'show_email': row[10],
            'show_phone': row[11],
            'show_hostname': row[12],
            'show_link': row[13]
        }
        shows.append(show)

    return shows

