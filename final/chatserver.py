import _thread
import socket
import json
import zlib

HOST = 'localhost'
PORT = 7778

clients = {}

def open_connection(data, sock):
    '''Opens the connection for the client
    
    To be used when there is a new connection recieved 
    and assigns that connection to a new client
    '''
    # removes all spaces
    username = data[1].replace(" ", "_")
    print(username, " connected")
    clients[username] = sock

    #dumping all data to json and encoding
    json_data = json.dumps(username + "has connected").encode('utf-8')

    #sending the len of the message first per assignment requirments
    data = len(json_data).to_bytes(4, 'big') + json_data
    # https://www.tutorialspoint.com/python/dictionary_items.htm
    for user, conn in clients.items():
        try:
            conn.sendall(data)
        except Exception:
            # removes the user from clients
            del clients[user]


def close_connection(data):
    '''Handles closing connection'''

    clients[data[1]].close()
    del clients[data[1]]
    json_data = json.dumps(data[1] + " has disconnected").encode('utf-8')
    data = len(json_data).to_bytes(4, 'big') + json_data

    for user, conn in clients.items():
        try:
            conn.sendall(data)
        except Exception:
            del clients[user]  


def broadcast_message(data):
    '''Handles Broadcasting messasges to all users'''
    # The user sends an example of "[BROADCAST, Liam, 'test]"
    json_data = json.dumps(str(data[1]) + "> " + str(data[2])).encode('utf-8')
    data = len(json_data).to_bytes(4, 'big') + json_data
    for user, conn in clients.items():
        try:
            conn.sendall(data)
        except Exception:
            del clients[user]


def private_message(data):
    # [Private, user1, message, user2]
    json_data = json.dumps(str(data[1]) + '>' + str(data[2])).encode('utf-8')
    data = len(json_data).to_bytes(4, 'big') + json_data

    # sending to both users so they can both see it
    # uses two separate try excepts so if one user crashes/disconnects
    # it can be removed
    try:
        clients[data[1]].sendall(data)
    except Exception:
        del clients[data[1]]
    try:
        clients[data[3]].sendall(data)
    except Exception:
        del clients[data[3]]


def handle_message(conn, addr):
    try:
        while True:
            msg_size = int.from_bytes(conn.recv(4), 'big')
            data = json.loads(conn.recv(msg_size).decode('utf-8'))
            first_index = data[0].upper()
            if first_index == 'START':
                open_connection(data, conn)
            elif first_index == 'EXIT':
                close_connection(data)
            elif first_index == 'BROADCAST':
                broadcast_message(data)
            elif first_index == 'PRIVATE':
                broadcast_message(data)
            else:
                conn.close()
                break
    except Exception:
        conn.close()
                

if __name__ == "__main__":

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(40)
    while True:
        try:
            client, addr = sock.accept()
            # creates a new thread for each client
            _thread.start_new_thread(handle_message, (client, addr))
        except:
            sock.close()
            print("Closing Down")
            break    