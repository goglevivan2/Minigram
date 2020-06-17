from PyQt5 import QtWidgets,QtCore
import clientui
import requests
import datetime
class ExampleApp(QtWidgets.QMainWindow,clientui.Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)
        self.url = url
        self.chanel = 'hub'
        self.pushButton.pressed.connect(self.send_message)
        self.pushButton_2.pressed.connect(self.changeChanel)
        self.last_timestamp = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def changeChanel(self):
        self.chanel = self.lineEdit_3.text()
        self.textBrowser.clear()
        response = requests.get(
            self.url + '/get_messages',
            params={'after': 0.0, 'chanel': self.chanel}
        )
        messages = response.json()['messages']

        for message in messages:
            dt = datetime.datetime.fromtimestamp(message['timestamp'])
            dt = dt.strftime('%H:%M:%S %d/%m/%Y')
            self.textBrowser.append('<div class="container"><h4>'+f'@{message["chanel"]}: ' + message['username'] + '</h4><p>' + message[
                'text'] + '</p><span class="date-right">' + dt + '</span></div>')
            self.textBrowser.append('\n')
            self.last_timestamp = message['timestamp']

    def send_message(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.textEdit.toPlainText()
        chanel = self.chanel
        if chanel =='':
            chanel = 'hub'
        #pass
        #message
        requests.get(
            self.url+'/send_message',
            json={
                'username': username,
                'password': password,
                'text': text,
                'chanel':chanel,
            }
        )
        self.textEdit.setText('')

    def update_messages(self):
        response = requests.get(
            self.url+'/get_messages',
            params={'after': self.last_timestamp,'chanel':self.chanel}
        )
        messages = response.json()['messages']

        for message in messages:

            dt = datetime.datetime.fromtimestamp(message['timestamp'])
            dt = dt.strftime('%H:%M:%S %d/%m/%Y')
            self.textBrowser.append('<div class="container"><h4>' +f'@{message["chanel"]}: '+ message['username']+'</h4><p>'+message['text']+'</p><span class="date-right">'+dt+'</span></div>')
            self.textBrowser.append('\n')
            self.last_timestamp = message['timestamp']








app =QtWidgets.QApplication([])
window=ExampleApp('http://goglevivan.pythonanywhere.com')
window.setFixedSize(497, 713)
window.show()
app.exec_()