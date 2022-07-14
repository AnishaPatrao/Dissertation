import eventlet #pip install -U eventlet
import socketio #pip install "python-socketio[client]"

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('my event', {'data': 'foobar1'})
    sendServo()

def sendServo():
    print("inside sendDervo")
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    connect()
    sio.emit('my event', {'data': 'foobar2'})

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)



#if __name__ == '__main__':
    
#eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
#sio.emit('my event', {'data': 'foobar3'})
#sendServo()

#sio.emit('my_message', {'data': 'foobar4'})
