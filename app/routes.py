from sqlalchemy.sql.functions import random
import json

from app import app
from flask import render_template, flash, redirect, url_for
import random

import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User

from flask_login import current_user, login_user, logout_user, login_required


def code():
    random_room = random.randint(10000, 99999)
    return random_room


rooms = []


@app.route('/index')
@app.route('/')
def index():
    return redirect("menu.html")


@app.route('/createrooms')
def game():
    game_room = {'key': code(),
                 'players': '',
                 'board': [
                     ['', '', ''],
                     ['', '', ''],
                     ['', '', '']
                 ]}

    rooms.append(game_room)

    with open("trade.json", "w", encoding="utf-8") as json_file:
        json.dump(rooms, json_file, ensure_ascii=False)

    print(rooms)
    return render_template("krestikiNoliki.html")



