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
