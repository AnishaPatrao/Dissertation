import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my_message', {'response': 'my response2'})

@sio.on('my event')
def on_message(data):
    print('I received a message!', data)

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('ws://raspberrypi2.local:5000')

def SendPosture(currentPosture):
    sio.emit('my_message', {'response': currentPosture})