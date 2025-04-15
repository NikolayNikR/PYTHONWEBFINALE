from sqlalchemy.sql.functions import random

from app import app
from flask import render_template, flash, redirect, url_for
import random

import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models import User

from flask_login import current_user, login_user, logout_user, login_required


def code():
    random_room = random.randint(10000, 99999)
    return  random_room


rooms = {}


@app.route('/index')
@app.route('/')
def index():
    return render_template("menu.html")


@app.route('/createrooms')
def game():
    game_room = {'key': code(),
                 'players': '',
                 'board': [
                     ['', '', ''],
                     ['', '', ''],
                     ['', '', '']
                 ]}
    rooms.update(game_room)
    print(rooms)
    return render_template("krestikiNoliki.html")
