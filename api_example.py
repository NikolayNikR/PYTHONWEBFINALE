from flask import Flask, redirect, url_for, request, jsonify, session
import json
import random
import string
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['ROOMS_FILE'] = 'rooms_button.json'

def load_rooms():
    if os.path.exists(app.config['ROOMS_FILE']):
        with open(app.config['ROOMS_FILE'], 'r') as f:
            return json.load(f)
    return {}

def save_rooms():
    with open(app.config['ROOMS_FILE'], 'w') as f:
        json.dump(rooms, f)

rooms = load_rooms()

def generate_room_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=4))
        if code not in rooms:
            return code

@app.route('/')
def index():
    return '''
    <h1>Кнопка в комнате</h1>
    <a href="/create">Создать комнату</a>
    <form action="/join" method="POST">
        <input type="text" name="room_code" placeholder="Код комнаты" maxlength="4" required>
        <button type="submit">Присоединиться к комнате</button>
    </form>
    '''

@app.route('/create', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        room_code = generate_room_code()
        rooms[room_code] = {
            "pressed": False
        }
        save_rooms()
        return redirect(url_for('room', room_code=room_code))
    return '''
    <form method="POST">
        <button type="submit">Создать новую комнату</button>
    </form>
    '''

@app.route('/join', methods=['POST'])
def join_room():
    room_code = request.form['room_code'].upper()
    if room_code in rooms:
        return redirect(url_for('room', room_code=room_code))
    else:
        return 'Комната не найдена! <a href="/">На главную</a>'

@app.route('/room/<room_code>')
def room(room_code):
    if room_code not in rooms:
        return "Комната не найдена", 404

    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Комната {room_code}</title>
        <style>
            #the-button {{
                font-size: 24px;
                padding: 20px 40px;
                color: white;
                border: none;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <h1>Комната {room_code}</h1>
        <button id="the-button">Загрузка...</button>
        <p id="state-text"></p>
        <script>
            const roomCode = "{room_code}";

            async function fetchButtonState() {{
                const resp = await fetch(`/api/room/${{roomCode}}/button_state`);
                if (resp.ok) {{
                    const data = await resp.json();
                    updateButton(data.pressed);
                }}
            }}

            async function toggleButton() {{
                const resp = await fetch(`/api/room/${{roomCode}}/toggle_button`, {{
                    method: 'POST'
                }});
                if (resp.ok) {{
                    const data = await resp.json();
                    updateButton(data.pressed);
                }}
            }}

            function updateButton(pressed) {{
                const btn = document.getElementById('the-button');
                const stateText = document.getElementById('state-text');
                if (pressed) {{
                    btn.textContent = "Отжать";
                    btn.style.backgroundColor = "green";
                    stateText.textContent = "Кнопка нажата";
                }} else {{
                    btn.textContent = "Нажать";
                    btn.style.backgroundColor = "red";
                    stateText.textContent = "Кнопка не нажата";
                }}
            }}

            document.getElementById('the-button').onclick = toggleButton;

            setInterval(fetchButtonState, 100);
            fetchButtonState();
        </script>
    </body>
    </html>
    '''

# API: Получить состояние кнопки
@app.route('/api/room/<room_code>/button_state')
def button_state(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404
    return jsonify({"pressed": rooms[room_code]['pressed']})

# API: Переключить кнопку
@app.route('/api/room/<room_code>/toggle_button', methods=['POST'])
def toggle_button(room_code):
    if room_code not in rooms:
        return jsonify({"error": "Комната не найдена"}), 404
    rooms[room_code]['pressed'] = not rooms[room_code]['pressed']
    save_rooms()
    return jsonify({"pressed": rooms[room_code]['pressed']})

if __name__ == '__main__':
    app.run(debug=True)
