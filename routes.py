import os
from idlelib.editor import keynames
from math import trunc

from sqlalchemy.sql.functions import random
import json

from app import app
from flask import render_template, Flask, redirect, url_for, request, jsonify
import random


def chek(code):
    board = rooms[code]['board']

    # Все выигрышные линии: 3 строки, 3 столбца, 2 диагонали
    lines = []

    # строки
    lines.extend(board)

    # столбцы
    for col in range(3):
        lines.append([board[row][col] for row in range(3)])

    # диагонали
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    # Проверяем, есть ли линия с тремя одинаковыми символами, не пустыми
    for line in lines:
        if line[0] != "" and line.count(line[0]) == 3:
            return True

    return False


def save_rooms():
    with open(app.config['ROOMS_FILE'], 'w') as f:
        json.dump(rooms, f)


def load_rooms() -> object:
    if os.path.exists(app.config['ROOMS_FILE']):
        with open(app.config['ROOMS_FILE'], 'r') as f:
            return json.load(f)
    return {}


rooms = load_rooms()
print(chek("22757"))


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


from flask import session
import uuid


@app.route('/room/<room_code>')
def room(room_code):
    if room_code not in rooms:
        return "Комната не найдена", 404

    room = rooms[room_code]

    # Получаем player_id из сессии или создаём новый
    player_id = session.get('player_id')

    if not player_id or session.get('room_code') != room_code:
        player_id = str(uuid.uuid4())
        session['player_id'] = player_id
        session['room_code'] = room_code

    # Если игрок ещё не в комнате - добавляем
    if player_id not in room['players']:
        if len(room['players']) < 2:
            # Назначаем символ X или O
            assigned_symbols = set(room['players'].values())
            symbol = 'X' if 'X' not in assigned_symbols else 'O'
            room['players'][player_id] = symbol
            save_rooms()
        else:
            # Комната заполнена
            return '''
            <!doctype html>
            <html><body>
            <h1>Комната заполнена</h1>
            <p>В комнате уже играют два игрока.</p>
            <a href="/">Вернуться на главную</a>
            </body></html>
            '''

    player_symbol = room['players'][player_id]
    return render_template('krestikiNoliki.html', room_code=room_code)

@app.route('/api/room/<room_code>/move', methods=['POST'])
def make_move(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404

    data = request.get_json()
    index1 = data.get('index')
    symbol = data.get('symbol')

    if index1 is None or symbol not in ['X', '0']:
        return jsonify({"error": "Неверные данные"}), 400

    row, col = divmod(index1, 3)
    board = rooms[room_code]['board']

    if board[row][col] != '':
        return jsonify({"error": "Ячейка уже занята"}), 400

    board[row][col] = symbol
    save_rooms()

    # Проверяем победу
    if chek(room_code):
        winner = symbol
    else:
        winner = None

    return jsonify({'board': board, 'winner': winner})
