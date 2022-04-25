from logging import debug
from flask import Flask,redirect,url_for, render_template,request, jsonify, make_response
from flask.wrappers import Response
from flask_socketio import SocketIO, send
import sys,requests
from requests.sessions import merge_setting


plain=""
n=90
enc_session={"status":False,"p":0,'z':[],"g":0,"a":0,"y":0,"k":0,"key_dec":0,"key_bin":"","p_q":0}
global home
home={"name":"","port":False}
target={"name":"","port":False}
connected={"status":"","port":"","user":""}
sendingMessage=""
receivingMessage=""


app=Flask(__name__)
socketio = SocketIO(app,  cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    global home
    home['name']=request.form.get('name')
    return render_template("apply.html", name=home['name'], port=home['port'])

@app.route('/search', methods=['POST'])
def search():
    global home
    global target
    target['port']=request.form.get('port')
    payload={'message':'connection_request','port':home["port"]}
    r=requests.post(f'http://127.0.0.1:{target["port"]}/connection',data=payload)
    stringifiesJson=r.json()
    target['name']=stringifiesJson['name']
    return render_template('chatbox.html', 
        name=home['name'],targetUser=stringifiesJson['name'],targetPort=stringifiesJson['port'])

@app.route('/connection', methods=['POST'])
def connection():
    global home
    return home

""" @app.route('/chat', methods=['POST'])
def chat():
    global home
    home['name']=request.form.get('name')
    return render_template("chatbox.html", name=home['name']) """


@app.route('/receive', methods=['POST'])
def receive():
    global home
    global target
    type=request.form.get("type")
    if type=='msg':
        print(request.form.get('message'))
        socketio.send(target["name"]+": "+request.form.get('message')+"\n")
    elif type=='connection':
        target['port']=request.form.get('port')
    return "received"

@socketio.on('message')
def handle_message(msg):
    global home
    global sendingMessage
    if msg['type']=='connection':
        home["port"]=msg['port']
        send("you can now chat!"+'\n')
    elif msg['type']=='msg':
        payload={'type':'msg','message':msg['body'],'port':home["port"]}
        r=requests.post(f'http://127.0.0.1:{target["port"]}/receive',data=payload)
        send(home["name"]+": " +msg['body']+"\n")

if __name__=="__main__":
    global port
    #port=False
    if len(sys.argv)<2:
        home['port']=input("enter port:")
    else:
        home['port']=sys.argv[1]
    socketio.run(app,host='127.0.0.1', port=home['port'])