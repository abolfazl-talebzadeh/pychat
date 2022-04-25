from logging import debug
from flask import Flask,redirect,url_for, render_template,request, jsonify, make_response
from flask_socketio import SocketIO, send
import sys,requests


plain=""
n=90
enc_session={"status":False,"p":0,'z':[],"g":0,"a":0,"y":0,"k":0,"key_dec":0,"key_bin":"","p_q":0}
home={"name":"","port":""}
connected={"status":"","port":"","user":""}
d_port=""
sendingMessage=""
receivingMessage=""


app=Flask(__name__)
socketio = SocketIO(app,  cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST','GET'])
def register():
    global port
    name=request.form.get('name')
    home['name']=name
    home['port']=port
    return render_template('apply.html', server=home['port'], name=home['name'] )
    #return render_template('chatbox.html', name=home['name'])

@app.route('/search', methods=['POST','GET'])
def search():
    global home
    global d_port
    d_port=request.form.get('port')
    payload={'message':'connection_request','port':home["port"]}
    r=requests.post(f'http://127.0.0.1:{d_port}/connection',data=payload)
    stringifiesJson=r.json()
    #header=f"the user {r1['name']} is register in port {r1['port']}"
    return render_template('chatbox.html', 
        name=home['name'],targetUser=stringifiesJson['name'],targetPort=stringifiesJson['port'])


@app.route('/connection', methods=['POST'])
def connection():
    message=request.form.get('message')
    return home

@app.route('/receive')
def receive():
    global receivingMessage
    #receivingMessage=request.form.get('message')
    #socketio.send(receivingMessage)
    return "received"

@socketio.on('message')
def handle_message(msg):
    global home
    global sendingMessage
    if msg['type']=='connection':
        send("you can now chat!"+'\n')
    elif msg['type']=='msg':
        sendingMessage=msg['body']
        payload={'message':msg['body']}
        #r=requests.post(f'http://127.0.0.1:{d_port}/receive',data=payload)
        #send(home["name"]+": "+ msg['body']+'\n')

if __name__=="__main__":
    global port
    port=False
    if len(sys.argv)<2:
        while not port:
            port=input("enter port:")
    else:
        port=sys.argv[1]
    #app.run('127.0.0.1',port,debug=True)
    socketio.run(app,host='127.0.0.1', port=port)  