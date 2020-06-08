from flask import Flask, request
from datetime import datetime
import time

app = Flask(__name__)
server_start = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
messages = [
    #{'username': 'jack', 'text': 'Hello everyone!', 'timestamp': time.time()},
    #{'username': 'jack2', 'text': 'Hello jack!', 'timestamp': time.time()},
]
# лучше в таком виде пароли не хранить
users = {
    'jack': '12345',
    'jack2': '12345',
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
        messages.append({"username": username, "text": result_text, "timestamp": time.time()})
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
        result = []
        for message in messages:
            if message['timestamp'] > after:
                result.append(message)
        return {
            "messages": result,
            "error": None
        }
    except Exception as e:
        return{ "messages":None,"error":e}



app.run(debug=True)