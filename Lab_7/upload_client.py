"""Client for Lab 7 reguarding sending files.

Author: Liam Cannon
Class: CSI-275
Assignment: Lab/HW 7
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
import argparse
import socket
import os
import constants


class UploadError(Exception):
    """Error when uploading."""

    pass


class UploadClient:
    """Upload Client for sending files to the server."""

    def __init__(self, host, port):
        """Init function for the Upload Client class."""
        address_tuple = (host, port)
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.settimeout(constants.MAX_TIMEOUT)
        try:
            self.tcp_sock.connect(address_tuple)
        except Exception:
            raise ConnectionError()
        self.buffer = b''

    def close(self):
        """Close handles closing the socket."""
        self.tcp_sock.close()

    def recv_all(self, length):
        """Recvs all the data and checks length."""
        data = b''
        while len(data) < length:
            more = self.tcp_sock.recv(length - len(data))
            if not more:
                # no matter how i indent this it no worko
                raise EOFError('expected %d bytpes but only recieved'
                                '%d bytes before the socket closed'
                                % (length, len(data)))      
            data += more
        return data

    def recv_until_delimiter(self, delimiter):
        """Recieves data until a delimiter and returns such."""
        while True:
            if delimiter in self.buffer:
                index = self.buffer.index(delimiter)
                temp = self.buffer[:index]
                self.buffer = self.buffer[index + 1:]
                return temp
            data = self.tcp_sock.recv(constants.MAX_BYTES)
            if not data:
                raise EOFError
            self.buffer += data

    def list_files(self):
        """List files handles listing all files sent to server."""
        self.tcp_sock.sendall("LIST\n".encode("UTF-8"))
        data = self.recv_until_delimiter(b'\n')
        file_list = []
        while not data:
            if data == "ERROR":
                raise UploadError
            data = data.decode("UTF-8")
            data = data.split(' ')
            file_list.append(str(data[0]), int(data[1]))
            data = self.recv_until_delimiter(b'\n')
        return file_list

    def upload_file(self, file_path):
        """Upload a file to the class's server.

        The function handles Q4 of the original assignment.
        """
        # Open the file
        file = open(file_path, "rb")

        # Read the whole thing into memory
        file_data = file.read()

        # Prep the first line to send
        header = "UPLOAD " + os.path.basename(file_path) + " " \
                 + str(len(file_data)) + "\n"
        print(f"Sending {header}")

        # TODO: Change tcp_sock here to match your __init__ function!
        self.tcp_sock.sendall(header.encode("ascii"))

        # TODO: Change tcp_sock here to match your __init__ function!
        # Send the file data
        self.tcp_sock.sendall(file_data)

        # Wait for a response
        return_msg = self.recv_until_delimiter(b"\n").decode("ascii")
        if return_msg == "ERROR":
            raise UploadError
        else:
            print("Upload successful")


def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    parser = argparse.ArgumentParser(description="TCP File Uploader")
    parser.add_argument("host", help="interface the server listens at;"
                        " host the client sends to")
    parser.add_argument("-p", metavar="PORT", type=int,
                        default=constants.UPLOAD_PORT,
                        help=f"TCP port (default {constants.UPLOAD_PORT})")
    args = parser.parse_args()
    upload_client = UploadClient(args.host, args.p)
    upload_client.upload_file("upload_client.py")
    print(upload_client.list_files())
    upload_client.close()


if __name__ == "__main__":
    main()