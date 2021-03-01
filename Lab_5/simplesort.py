"""Don't forget your docstring!"""
import socket
HOST = "localhost"
PORT = 20000

class SortServer:    
    """Don't forget your docstring!"""  
    def __init__(self, host, port):        
        "Don't forget your docstring!" 
        #assigning variables and init sock
        self.address_tuple = (host, port)
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.bind(self.address_tuple)
               
        pass  

    def run_server(self):        
        """Don't forget your docstring!"""
        self.tcp_sock.listen(20)
        while True:
            print("waiting")
            client_sock, address = self.tcp_sock.accept()
            client_sock.settimeout(1)
            while True:
                data = client_sock.recv(4096)
                data = data.decode("ascii")
                if not data.startswith("LIST "):
                    client_sock.sendall("ERROR".encode("ascii"))
                if data.startswith("LIST "):
                    #if the data starts with list then this just gets rid of that and the space
                    data = data[5:]
                try:
                    #default sort type
                    sort_type = 'a'
                    #splitting to check for pipe
                    split = data.split('|')
                    data = split[0]
                    if len(split) == 2:
                        #if the split len is 2 then there is a pipe
                        sort_type = split[1]
                    if sort_type == 'a':
                        data = [float(i) for i in data]
                        data.sort()
                        client_sock.sendall(("SORTED " + data).encode("ascii"))
                    elif sort_type == 'd':
                        data = [float(i) for i in data]
                        data.sort(reverse=True)
                        client_sock.sendall(("SORTED " + data).encode("ascii"))
                    elif sort_type == 's':
                        data.sort()
                        client_sock.sendall(("SORTED " + data).encode("ascii"))
                except ValueError:
                    client_sock.sendall(("ERROR").encode("ascii"))
        
if __name__ == "__main__":    
    server = SortServer(HOST, PORT)    
    server.run_server()


    """
    tcp_sock = socket.socket(AF_NET, Stream or somthing like that)
    address_tuple = (host, port)
    tcp_sock.bind(address_tuple)
    tcp_sock.listen(20)
    client_sock, address = tcp_sock.accept()
        put in loop while True:
    while True:
        data = connection.recv(4096)
        if not data:
            break
    data = client_sock.recv(4096)
    response = "Yep cock"
    client_sock.sendall(response.encode("ascii))
    """