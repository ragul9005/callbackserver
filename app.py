from flask import Flask, request, render_template
from flask_sock import Sock
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)  # This will set up ngrok for you
sock = Sock(app)

clients = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def receive_post():
    data = request.get_json()  # Get the JSON data
    print(data)  # Print it to the console

    # Notify all connected clients with the received data
    for client in clients:
        client.send(str(data))  # Convert to string to send via WebSocket

    return {"message": "Data received!"}, 200

@sock.route('/ws')
def websocket(ws):
    clients.append(ws)  # Add the new client to the list
    try:
        while True:
            msg = ws.receive()  # Keep the connection open
            if msg is None:
                break
    finally:
        clients.remove(ws)  # Remove the client when disconnected

if __name__ == '__main__':
    # No need for host='0.0.0.0' here
    app.run()  # Ngrok will handle the URL exposure
