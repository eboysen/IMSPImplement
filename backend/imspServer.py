import socketserver
import threading

class IMSPRequestHandler(socketserver.BaseRequestHandler):
    def _init_(self,request,client_address,server):
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return
    def setup(self):
        print('setup request')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        print('handle request')

        # Echo the back to the client
        data = self.request.recv(1024)
        print(data.decode())
        data = data.decode()
        line1 = data[0:data.find('\n')]
        print('firstLine:'+line1)
        if(line1 == 'CHECK'):
            data = '200'
        self.request.send(str.encode(data))
        return

    def finish(self):
        print('finished request')
        return socketserver.BaseRequestHandler.finish(self)

class IMSPServer(socketserver.TCPServer):
    def __init__(self, server_address, handler_class=IMSPRequestHandler):
        print('IMSP server initialized')
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        print('IMSP server running')
        socketserver.TCPServer.server_activate(self)
        return

    def serve_forever(self):
        print('IMSP server running')
        while True:
            self.handle_request()
        return

    def handle_request(self):
        print('handling request\n')
        return socketserver.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        print('verifying request\n')
        return socketserver.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        print('processing request\n')
        return socketserver.TCPServer.process_request(self, request, client_address)

    def server_close(self):
        print('closing server\n')
        return socketserver.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        print('finished request')
        return socketserver.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):
        print('closed request')
        return socketserver.TCPServer.close_request(self, request_address)

address = ('localhost',10000)
server = IMSPServer(address,IMSPRequestHandler)
ip, port = server.server_address
print('ip'+ip)
print(port)
t = threading.Thread(target=server.serve_forever)
t.start()
