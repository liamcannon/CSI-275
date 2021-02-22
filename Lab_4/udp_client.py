"""Liam Cannon Lab 4's code includes the use of UDP ports to send and recieve.

Author: Liam Cannon
Class: CSI-275-01
Assignment: Lab_4
Due Date: 2/22/2021
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
import constants
import random
"""Student code for Lab/HW 2.

Champlain College CSI-235, Spring 2019
The following code was written by Joshua Auerbach (jauerbach@champlain.edu)
"""


class UDPClient:
    """UDPClient Class for establishing and sending data using UDP.

    Includes send_message, send_message_by_character, and an init
    """

    udp_sock = None
    udp_host = None
    udp_port = None
    udp_request_id = None

    def __init__(self, host, port, request_id=False):
        """Init function for when the class is called.

        allows for variables to be assigned.
        """
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_host = host
        self.udp_port = port
        self.udp_request_id = request_id

    def send_data(self, c):
        wait_time = constants.INITIAL_TIMEOUT
        response_str = ""
        while True:
            try:
                self.udp_sock.settimeout(wait_time)
                if self.udp_request_id:
                    req_id = random.randint(0, constants.MAX_ID)
                    data = (str(req_id)) + "|" + c
                    self.udp_sock.sendto(data.encode("ascii"), (
                        self.udp_host, self.udp_sock))
                    response, address = self.udp_sock.recvfrom(
                        constants.MAX_BYTES)
                else:
                    self.udp_sock.sendto(c.encode("ascii"), (
                        self.udp_host, self.udp_port))
                    response, address = self.udp_sock.recvfrom(1)

                response = response.decode("ascii")

                if self.udp_request_id:
                    if req_id == int(response.split("|")[0]):
                        response_str += response.split("|")[1]
                    else:
                        continue
                else:
                    response_str += response
            except socket.timeout:
                if wait_time >= constants.MAX_TIMEOUT:
                    raise(TimeOutError)
                wait_time *= 2
                if wait_time > constants.MAX_TIMEOUT:
                    wait_time = constants.MAX_TIMEOUT
                return response_str

    def send_message_by_character(self, data):
        """Send message by character for param data.

        iterates through the param data and calls send_message
        """
        for c in data:
            self.send_data(c)

class TimeOutError(Exception):
    """Used for When the UDP socket times out."""

    pass


def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    client = UDPClient(constants.HOST, constants.ECHO_PORT)
    print(client.send_message_by_character("hello world"))

    client = UDPClient(constants.HOST, constants.REQUEST_ID_PORT, True)
    print(client.send_message_by_character("hello world"))


if __name__ == "__main__":
    main()
