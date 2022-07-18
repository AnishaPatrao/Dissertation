import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    sio.emit('my_message', {'response': 'my response1'})


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

sio.connect('ws://raspberrypi.local:5000')
#sio.wait()

count = 1
while count < 5:
    sio.emit('my_message', {'response': 'my response3'})
    count = count + 1