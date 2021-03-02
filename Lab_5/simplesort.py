"""Don't forget your docstring!"""
import socket
HOST = "localhost"
PORT = 20000

def remove_point_zero(value):
  value = str(value)
  if value.endswith(".0"):
    return value[:-2]
  return value

class SortServer:    
    """class for establishing a sorting server."""  
    def __init__(self, host, port):        
        "Init function for establishing variables." 
        #assigning variables and init sock
        self.address_tuple = (host, port)
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.bind(self.address_tuple)
               
        pass  
    def handle_data(self, data):
        """ Handle data deals with organization and validating of data."""
        split_data = data.split("|")
        sort_type = "a"
        #checks if there is a pipe and splits data and sort type 
        if len(split_data) == 2:
            sort_type = split_data[1]
            data = split_data[0]
        data = data.split(" ")

        try:
            #catches all the errors possible 
            #LIST not there, only LIST there, checking to make sure
            # theres a valid pipe char
            if not data[0] == "LIST":
                return "ERROR"
            data = data[1:]
            if len(data) == 0:
                return "ERROR"
            if sort_type == "a":
                #casting as float
                data = [float(i) for i in data]
                data.sort()
            elif sort_type == "d":
                #casting as float
                data = [float(i) for i in data]
                data.sort(reverse=True)
            elif sort_type == "s":
                data.sort()
            else:
                return "ERROR"
        except ValueError:
            return "ERROR"
        #used to remove .0's from floats 
        data = [remove_point_zero(i) for i in data]
        data = [str(i) for i in data]
        data = " ".join(data)
        data = "SORTED " + data
        return data

    def run_server(self):        
        """Runs the server waits for client and relys on handle data to do the rest."""
        self.tcp_sock.listen(20)
        while True:
            print("waiting")
            client_sock, address = self.tcp_sock.accept()
            client_sock.settimeout(1)
            while True:
                data = client_sock.recv(4096)
                data = data.decode("ascii")
                try:
                    #passes off data to handle data to keep things organized
                    data = self.handle_data(data)
                    client_sock.sendall(data.encode("ascii"))
                except ValueError:
                    client_sock.sendall("ERROR".encode("ascii"))
        
if __name__ == "__main__":    
    server = SortServer(HOST, PORT)    
    server.run_server()