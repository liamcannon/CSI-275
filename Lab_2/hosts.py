"""Liam Cannons code for Lab 2

Author: Liam Cannon
Class: CSI-275-01
Assignment: Lab2
Due Date: 2/8/2021
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


"""Student code for Lab/HW1.

    Run python autograder.py

Champlain College CSI-235, Spring 2019
The following code was written by Joshua Auerbach (jauerbach@champlain.edu)
Host class __init__ function by Jason Reeves 1/4/2021 (reeves@champlain.edu)
"""

from util import raise_not_defined


class InvalidEntryError(Exception):
    """Exception raised for invalid entries in the hosts file."""

    pass


def is_valid_ip_address(ip_address):
    """Return whether the given ip_address is a valid IPv4 address or not.

    Args:
        ip_address (str): ip_address to test

    Returns:
        bool: True if ip_address is valid IPv4 address, False otherwise.

    """
    #   *** YOUR CODE HERE ***
    """
    counter = 0
    for c in ip_address:
        if(c.isalpha() and c != "."):
            return False
        else:
            if(c == "."):
                counter += 1
    if(counter == 3):
        return True
    else:
        return False
    """
    ip_address = str(ip_address).split('.')
    if(len(ip_address) != 4):
        return False
    for x in ip_address:
        print(x)
        try:
            num = int(x)
            if num > 255 or num < 0:
                return False
        except ValueError:
            return False
    return True

def is_valid_hostname(hostname):
    """Return whether the given hostname is valid or not.

    Host names may contain only alphanumeric characters, minus signs ("-"),
    and periods (".").  They must begin with an alphabetic character and end
    with an alphanumeric character.

    Args:
        hostname (str): hostname to test

    Returns:
        bool: True if hostname is valid, False otherwise.

    """
    #   *** YOUR CODE HERE ***
    if len(hostname) == 0:
        return False
    if not hostname[0].isalpha():
        return False
    if not hostname[-1].isalnum():
        return False

    for c in hostname:            
        if not c == '.' and not c == '-':
            if not c.isalnum():
                return False
    return True
    

class Hosts:
    """The Hosts class handles translating hostnames to ip addresses."""

    def __init__(self, hosts_file):
        """Initialize the Hosts class.

        Imports all of the host names and addresses
        from the provided hosts_file. If the file does
        not follow the proper format or contains
        invalid IP addresses, hostnames, or aliases,
        an InvalidEntryError is raised.

        If successful, this function fills two lists
        (self.ips and self.hostnames) that together
        represent IP/hostname and IP/alias mappings
        in the parsed file. The hostname at index i
        in self.hostnames will correspond to the IP
        at index i in self.ips.

        For example, if the first line of a hosts file
        maps localhost to 127.0.0.1, then
        self.hostnames[0] = 'localhost' and
        self.ips[0] = '127.0.0.1'.
        """
        f = open(hosts_file, "r")

        self.ips = []
        self.hostnames = []

        line = f.readline()
        while line:
            # If the line is a comment, skip it
            if line[0] == "#":
                line = f.readline()
                continue

            # If the line is blank, skip it
            if line[0] == "\n":
                line = f.readline()
                continue

            # The first 16 characters represent the IP address
            ip_address = line[0:16]
            print(f"IP = {ip_address}")
            # Make sure to remove any trailing whitespace!
            if not is_valid_ip_address(ip_address.rstrip()):
                print("Bad IP")
                raise InvalidEntryError

            # The hostname is the first string
            # starting from the 17th character,
            # and aliases are anything after that
            rest_of_line = line[16:].split(" ")
            # hostname = rest_of_line[0]
            has_hostname = False
            for hostname in rest_of_line:
                print(hostname.rstrip())
                # If we see a comment, the rest of the line should be tossed
                if hostname.rstrip() == "#":
                    print("We're done here")
                    break
                if not is_valid_hostname(hostname.rstrip()):
                    print("Bad Hostname")
                    if hostname.rstrip() != "":
                        raise InvalidEntryError
                else:
                    # If we reach here, the line is valid, so
                    # add it to our mapping
                    has_hostname = True
                    self.ips.append(ip_address.rstrip())
                    self.hostnames.append(hostname.rstrip())

            # If we didn't find a hostname before,
            # raise an error
            if not has_hostname:
                raise InvalidEntryError

            # Read the next line
            line = f.readline()

    def contains_entry(self, hostname):
        """Return whether or not a given hostname exists."""
        #   *** YOUR CODE HERE ***
        if hostname in self.hostnames:
            return True
        return False


    def get_ip(self, hostname):
        """Return the IP for a given hostname.

        If the hostname does not exist in the file,
        None is returned.
        """
        #   *** YOUR CODE HERE ***
        if not hostname in self.hostnames:
            return None
        index = self.hostnames.index(hostname)

        return self.ips[index]
