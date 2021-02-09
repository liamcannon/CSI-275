"""Liam Cannons code for Lab 3.
Author: Liam Cannon
Class: CSI-275-01
Assignment: Lab_3
Due Date: 2/15/2021
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

sock = socket.socket()

def build_list():
    """Collect input from the user and return it as a list.    
    Only numeric input will be included; strings are rejected.    
    """

    unsortedArray = []
    coll_data = True
    while(coll_data):
        userInput = input("Enter Number for Array: ")
        try:
            check = int(userInput)
            unsortedArray.append(check)
        except Exception:
            try:
                check = float(userInput)
                unsortedArray.append(userInput)
            except Exception: 
                if(userInput == "done"):
                    coll_data = False
                else:
                    print("Not a Num")
    return unsortedArray

def sort_list(unsortedList):
    """ Takes in an unsorted list, connects to the required ipv4 address where the list is sent ordered and returned
    """
    print("unsorted:", unsortedList)
    sock.connect(("52.23.82.199", 7778))
    data = "LIST"
    for i in unsortedList:
        data += " " + str(i)
    raw_data = data.encode('ascii')
    sock.sendall(raw_data)
    raw_reply = "" #empty byte string
    while True:
        more = sock.recv(4096)
        if not more:
            break
        raw_reply += more.decode('ascii')
    sock.close()
    return raw_reply

def main():
    """Call the build_list and sort_list functions, and print the result."""    
    number_list = build_list()    
    print (sort_list(number_list))

if __name__ == "__main__":    
    main()

