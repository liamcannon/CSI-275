#File sort.py
#Lab_1 Sorting with Python
#Author Liam Cannon
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

