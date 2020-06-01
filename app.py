from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello()->str:
    '''
    Index page function
    '''
    return "Hello World"

@app.route('/status')
def status()->str:
    '''
       Index page function
    '''
    try:
        current_time = datetime.strftime(datetime.now(), "%H:%M:%S")
        return {
            "status": "OK",
            "name": "Minigram",
            "time": current_time
        }
    except Exception as e:
        return "You have some errors: "+str(e) # return info about some errors

app.run(debug=True)