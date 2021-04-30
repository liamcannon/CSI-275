'''
Author: Liam Cannon
Class : CSI-275
Assignment : Final
Date Due: 4/30/2021
  Description : Chat Client 
  Certification of Authenticity :
    I certify that this is entirely my own work, except where I have given
    fully - documented references to the work of others.I understand the
    definitionand consequences of plagiarismand acknowledge that the assessor
    of this assignment may, for the purpose of assessing this assignment :
    -Reproduce this assignmentand provide a copy to another member of
    academic staff;and /or
    -Communicate a copy of this assignment to a plagiarism checking
    service(which may then retain a copy of this assignment on its
      database for the purpose of future plagiarism checking)
'''

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
    while True:
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
        json_data = json.dumps(data).encode('utf-8')
        full_data = len(json_data).to_bytes(4, 'big') + json_data
        print("HERE", full_data)
        recv_data_sock.sendall(full_data)
    except Exception:
        recv_data_sock.close()
        send_data_sock.close()
        print('Closing connection')


def get_chat(chat):
    # checking if the message is greater than 0
    if len(chat) > 0 and chat[0] == '@':
        recipient = chat.split()[0][1:]
        chat = " ".join(chat.split()[1:])
        send_data(['PRIVATE', username, chat, recipient])
    elif chat == 'EXIT':
        send_data(['EXIT', username])
        send_data_sock.close()
        recv_data_sock.close()
    else:
        send_data(['BROADCAST', username, chat])


if __name__ == "__main__":
    username = input("Enter a display name: ")
    username = username.replace(' ', '_')
    chat_server()
    try:
        chat = input("Chat: ")
        get_chat(chat)
    except Exception:
        pass
    _thread.start_new_thread(recv_data, ())
    _thread.start_new_thread(send_data, ())
