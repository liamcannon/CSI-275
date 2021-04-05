"""Don't forget your docstrings!
"""
import json
import socket
import zlib

def build_list():
    """Collect input from the user and return it as a list.

    Only numeric input will be included; strings are rejected.
    """
    #Create a list to store our numbers
    unsorted_list = []

    # Create a variable for input
    user_input = ""
    sort_type = ""

    while sort_type.lower() != 'a' and sort_type.lower() != 'd' and sort_type.lower() != 's':
        sort_type = input("Please enter sort type, a, d, or s: ")  

    unsorted_list.append(sort_type)

    while user_input != "done":
        # Prompt the user for input
        user_input = input("Please enter a number, or 'done' to stop.")

        # Validate our input, and add it to out list
        # if it's a number
        try:
            # Were we given an integer?
            unsorted_list.append(int(user_input))
        except ValueError:
            try:
                # Were we given a floating-point number?
                unsorted_list.append(float(user_input))
            except ValueError:
                # Non-numeric input - if it's not "done",
                # reject it and move on
                if (user_input != "done"):
                    print ("ERROR: Non-numeric input provided.")
                continue

    # Once we get here, we're done - return the list
    return unsorted_list

def sort_list(unsorted_list):
    """Put your docstring here."""
    # YOUR SOCKET CODE GOES HERE!
    json_data = json.dumps(unsorted_list).encode('utf-8')
    #json_encoded = json_data.encode('utf-8')
    print("Uncompressed: ", len(json_data))
    json_data = zlib.compress(json_data)
    print("Compressed: ", len(json_data))

    json_sock = socket.socket()
    json_sock.connect(("localhost", 7778))
    print(json_data)
    json_sock.sendall(json_data)

    recv_data = json_sock.recv(4096).decode('utf-8')
    #recv_json = recv_data.decode('utf-8')
    
    recv_dict = json.loads(recv_data)

    json_sock.close()
    print(recv_dict)

def main():
    """Call the build_list and sort_list functions, and print the result."""
    #sort_type = input("Enter a sort type, a, d, or s: ")
    number_list = build_list()
    sort_list(number_list)

if __name__ == "__main__":
    main()

