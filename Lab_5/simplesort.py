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
                print("RECIEVED " + data)
                try:
                    data = data.split(" ")
                    print(type(data))
                    sort_type = 'a'
                    if not data[0] == "LIST":
                        return "ERROR"
                    #if the data starts with list then this just gets rid of that and the space
                    data = data[1:]
                    if len(data) == 0:
                        return "ERROR"
                    if "|" in data[-1]:
                        sort_type = data[-1][-1]
                        data[-1] = data[-1][:2]
                    #default sort type
                    #splitting to check for pipe
                    if sort_type == "a":
                        data = [float(i) for i in data]
                        """
                        for i in data:
                            data[i] = data[float(i)]
                        """
                        data.sort()
                    elif sort_type == "d":
                        data = [float(i) for i in data]
                        data.sort(reverse=True)
                    elif sort_type == "s":
                        #data = [str(i) for i in data]
                        data.sort()
                        print("S HERE 2")
                    data = [str(i) for i in data]
                    " ".join(data)
                    data.insert(0, "SORTED")
                    for i in data:
                        print(i)
                    client_sock.sendall(data.encode("ascii"))
                except ValueError:
                    return "ERROR"
        
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