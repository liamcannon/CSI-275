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

    def try_send(self, data):
        """Try send Attempts to send the data.

        errors if the socket timesout
        """
        self.udp_sock.settimeout(constants.INITIAL_TIMEOUT)
        while True:
            try:
                response = self.send_data(data)
                if response is None:
                    continue
                return response
            except socket.timeout:
                self.udp_sock.settimeout(self.udp_sock.gettimeout()*2)
                if(self.udp_sock.gettimeout() > constants.MAX_TIMEOUT):
                    raise TimeOutError()

    def send_data(self, data):
        """Send the data to the established host and port.

        separate from send by char to split up the work
        """
        req_id = 0
        if self.udp_request_id:
            req_id = random.randint(0, constants.MAX_ID)
            data = str(req_id) + "|" + data
        self.udp_sock.sendto(data.encode("ascii"), (
            self.udp_host, self.udp_port))
        response = self.udp_sock.recvfrom(
            constants.MAX_BYTES)[0].decode("ascii")
        if self.udp_request_id:
            response = response.split('|')
            if req_id == int(response[0]):
                return response[1]
        else:
            return response

    def send_message_by_character(self, data):
        """Send message by character for param data.

        iterates through the param data and calls send_message
        """
        response_str = ""
        try:
            for c in data:
                response_str += self.try_send(c)
        except TimeOutError:
            raise TimeOutError()
        return response_str
        # when running the questions individually they all work but for some reason when run together one of the tests in q1 fails

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
