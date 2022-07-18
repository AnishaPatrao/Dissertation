import eventlet #pip install -U eventlet
import socketio #pip install "python-socketio[client]"
import movement
import json

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    
@sio.event
def my_message(sid, data):
    strData = json.dumps(data)
    # parse x:
    posture = json.loads(strData)
    print(posture)
    # the result is a Python dictionary:
    movement.Move(posture["response"])

@sio.event
def disconnect(sid):
    print('disconnect ', sid)



if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


