"""Server for Lab 6 dealing with recv bytes size.

Author: Liam Cannon
Class: CSI-275
Assignment: Lab/HW 6 -- Framing with Length Fields

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""
import socket

HOST = "localhost"
PORT = 45000

def recvall(sock, length):
    """ Recvs all the data and checks length"""
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('expected %d bytpes but only recieved'
                            ' %d bytes before the socket closed'
                            % (length, len(data)))
        data += more
    return data

class LengthServer:
    """Create a server that return the length of received strings."""

    def __init__(self, host, port):
        """Init function of the Length Server Class"""
        self.address_tuple = (host, port)
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.bind(self.address_tuple)

    def calc_length(self):
        """Calc Length Handles the server and calculating the length"""
        self.tcp_sock.listen(20)
        while True:
            print("Waiting for Connection")
            client, address = self.tcp_sock.accept()
            self.tcp_sock.settimeout(1)
            #gets first 4 bytes
            data_length = client.recv(4)
            # converts
            data_length = int.from_bytes(data_length, 'big')
            try:
                data = recvall(client, data_length)
                # gets the total amount of bytes
                data = "I received " +  str(len(data)) + " bytes."
                print(data)
            except EOFError:
                # if error returns Length Error
                data = "Length Error"
            # putting this into one line with + data .encode on the end seemed to work
            # instead of having data.encode on a different line for some reason
            data = len(data).to_bytes(4, 'big') + data.encode("ascii")
            client.sendall(data)
        client.close()
   
if __name__ == "__main__":
    server = LengthServer(HOST, PORT)
    server.calc_length()