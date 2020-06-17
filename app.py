from flask import Flask, request
from datetime import datetime
import time

app = Flask(__name__)
server_start = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
messages = [
    {'username': 'Information', 'text': '''Это хаб для пользователей  тут можно общаться и искать каналы. 
    Для создания или перехода в канал необходимо ввести в поле chanel название канала и нажать на change.
    Вы всегда можете вернуться вписав в поле chanel название hub и нажать на change.''',
     'timestamp': time.time(),'chanel':'hub'},
]

users = {
    'Information': '1806f63b426354e43b75862eeccdd548b45f33830aed7f388432e6fe2794128a31379627d3f8bdb231cba902e8c28893',
}

@app.route('/')
def hello()->str:
    '''
    Index page function: no param
    -----------------------------
    [RU] Индексная страница.
    [EN] Index web page.
    -----------------------------
    '''
    return 'Hello, User! Это наш мессенджер. Его <a href="/status">статус</a>'

@app.route('/status')
def status()->str:
    '''
    Status page function: no param
    ------------------------------
    [RU] Данная функция показывает
    статус сервера.
    [EN] This function shows
    server status.
    ------------------------------
    '''
    try:
        status_message= {
            "status": "OK",
            "name": "Minigram",
            "server_start_time": server_start,
            "server_current_time": datetime.now().strftime('%H:%M:%S %d/%m/%Y'),
            "current_time_seconds": time.time(),
            "users_on_server":len(users),
            "messages_on_server":len(messages)
        }
        return status_message
    except Exception as e:
        return {"status":"ERROR","error":e}

@app.route("/send_message")
def send_message()->dict:
    '''
    Sending messages function: no param
    -----------------------------------
    [RU] Данная функция позволяет
    пользователю зайти либо
    зарегистрироваться и отправить
    сообщение.
    [EN] This function allows
    user to sign up or sign in
    and send some message.
    -----------------------------------
    '''
    try:
        username = request.json['username']
        password = request.json['password']
        text = request.json['text']
        chanel=request.json['chanel']
        if chanel == '':
            chanel = 'hub'

        if username in users:
            if users[username] != password:
                return {"ok": False,"error":"Incorrect password"}
        else:
            users[username] = password
        #анализ введённых команд
        array_of_words = text.split()
        result_text=''
        for word in array_of_words:
            if word =='!horse':
                result_text+= '🐴 '
            elif word == '!smile':
                result_text+= '🙂 '
            elif word == '!pistol':
                result_text+= '🔫 '
            else:
                result_text+=word+' '
        #это можно ещё и увеличить и добавить новое
        ########################
        messages.append({"username": username, "text": result_text, "timestamp": time.time(),"chanel":chanel})
        # text ?
        return {"ok": True, "error": None}
    except Exception as e:
        return {"ok":False,"error":e}






@app.route("/get_messages")
def get_messages()->dict:
    '''
    Getting messages function: no param
    -----------------------------------
    [RU] Данная функция выдаёт
    пользователю все актуальные
    сообщения с сервера.
    [EN] This function get to
    user all actually messages from
    server.
    -----------------------------------
    '''
    try:
        after = float(request.args['after'])
        ch =str(request.args['chanel'])
        result = []
        for message in messages:
            if message['timestamp'] > after and message['chanel'] == ch:
                result.append(message)
        return {
            "messages": result,
            "error": None
        }
    except Exception as e:
        return{ "messages":None,"error":e}



app.run(debug=True)