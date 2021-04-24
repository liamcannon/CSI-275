import _thread
import socket
import json

HOST = 'localhost'
PORT = 7778

username = ""

send_data_sock = socket.socket()
recv_data_sock = socket.socket()

def send_data(data):
    '''Handles sending all data'''
    json_data = json.dumps(data).encode('utf-8')
    full_data = len(json_data).to_bytes(4, 'big') + json_data
    send_data_sock.sendall(full_data)

def recv_data():
    '''Handles Recieving all data from server'''
    while True:
        data_size = int.from_bytes(recv_data_sock.recv(4), 'big')
        full_data = json.loads(recv_data_sock.recv(data_size).decode('utf-8'))
        print(full_data)

def chat_server():
    try:
        recv_data_sock.connect((HOST, PORT))
        send_data_sock.connect((HOST, PORT))
        data = ['START', username]
        json_data = json.dumps(full_data).encode('utf-8')
        full_data = len(json_data).to_bytes(4, 'big') + json_data
        recv_data_sock.sendall(full_data)
    except Exception:
        recv_data_sock.close()
        send_data_sock.close()
        print('Closing connection')

def get_chat():
    


if __name__ == "__main__":
    
