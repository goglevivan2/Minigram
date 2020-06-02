from flask import Flask, request
from datetime import datetime
import time
app = Flask(__name__)
server_start = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
messages = [
    {'username': 'jack', 'text': 'Hello everyone!', 'timestamp': time.time()},
    {'username': 'jack2', 'text': 'Hello jack!', 'timestamp': time.time()},
]
users = {
    'jack': '12345',
    'jack2': '12345',
}

@app.route('/')
def hello()->str:
    '''
    Index page function
    '''
    return 'Hello, User! Это наш мессенджер. Его <a href="/status">статус</a>'

@app.route('/status')
def status()->str:
    '''
       Index page function
    '''
    try:
        current_time = datetime.strftime(datetime.now(), "%H:%M:%S %d/%m/%Y")
        return {
            "status": "OK",
            "name": "Minigram",
            'server_start_time': server_start,
            'server_current_time': datetime.now().strftime('%H:%M:%S %d/%m/%Y'),
            'current_time_seconds': time.time()
        }
    except Exception as e:
        return "You have some errors: "+str(e) # return info about some errors

@app.route("/send_message")
def send_message():
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']

    if username in users:
        if users[username] != password:
            return {'ok': False}
    else:
        users[username] = password

    messages.append({'username': username, 'text': text, 'timestamp': time.time()})

    # text ?

    return {'ok': True}


@app.route("/get_messages")
def get_messages():
    after = float(request.args['after'])

    result = []

    for message in messages:
        if message['timestamp'] > after:
            result.append(message)

    return {
        'messages': result
    }

app.run(debug=True)