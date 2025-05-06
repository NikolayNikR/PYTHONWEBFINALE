import os
from idlelib.editor import keynames

from sqlalchemy.sql.functions import random
import json

from app import app
from flask import render_template, Flask, redirect, url_for, request, jsonify
import random


def save_rooms():
    with open(app.config['ROOMS_FILE'], 'w') as f:
        json.dump(rooms, f)


def load_rooms() -> object:
    if os.path.exists(app.config['ROOMS_FILE']):
        with open(app.config['ROOMS_FILE'], 'r') as f:
            return json.load(f)
    return {}


rooms = load_rooms()


def code():
    random_room = random.randint(10000, 99999)
    return str(random_room)


@app.route('/index')
@app.route('/')
def index():
    return render_template("menu.html")


@app.route('/create', methods=['GET', 'POST'])
def creategame():
    if request.method == 'POST':
        key = code()
        rooms[key] = {'players': {},
                      'board': [
                          ['', '', ''],
                          ['', '', ''],
                          ['', '', '']
                      ]}
        save_rooms()
        return redirect(url_for('room', room_code=key))


@app.route('/join', methods=['POST'])
def join_room():
    key = request.form['room_code']
    if key in rooms:
        return redirect(url_for('room', room_code=key))
    return "Комната не найдена", 404


@app.route('/room/<room_code>')
def room(room_code):
    if room_code not in rooms:
        return "Комната не найдена", 404
    return render_template('krestikiNoliki.html', room_code=room_code)


@app.route('/api/room/<room_code>')
def button_state(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404
    return jsonify({'board': rooms[room_code]['board']})


@app.route('/api/room/<room_code>', methods=['POST'])
def toggle_button(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404
    rooms[room_code]['board'] = not rooms[room_code]['board']
    save_rooms()
    return jsonify({'board': rooms[room_code]['board']})
