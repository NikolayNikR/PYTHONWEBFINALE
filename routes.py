import os

from sqlalchemy.sql.functions import random
import json

from app import app
from flask import render_template, Flask, redirect, url_for, request
import random



def code():
    random_room = random.randint(10000, 99999)
    return random_room


def save_rooms():
    with open(app.config['ROOMS_FILE'], 'w') as f:
        json.dump(rooms, f)



def load_rooms() -> object:
    if os.path.exists(app.config['ROOMS_FILE']):
        with open(app.config['ROOMS_FILE'], 'r') as f:
            return json.load(f)
    return {}


rooms = load_rooms()


@app.route('/index')
@app.route('/')
def index():
    return render_template("menu.html")


@app.route('/create', methods=['GET', 'POST'])
def creategame():
    if request.method == 'POST':
        room_code = code()
        rooms[room_code] = {'key': code(),
                            'players': {},
                            'board': [
                                ['', '', ''],
                                ['', '', ''],
                                ['', '', '']
                            ]}
        save_rooms()

    return render_template('krestikiNoliki.html')
