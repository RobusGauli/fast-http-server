from socket import socket
from socket import SOCK_STREAM, AF_INET
from httptools import HttpRequestParser
from one.request import Request
from one.log import log

import argparse

class CIDict(dict):
    def get(self, key, default=None):
        return super().get(key, default)
    
    def __getitem__(self, key):
        return super().__getitem__(key.casefold())
    
    def __setitem__(self, key, val):
        return super().__setitem__(key.casefold(), val)
    
    def __contains__(self, key):
        return super().__contains__(key.casefold())




class Server:

    def __init__(self, hostname, port, request_handler, request_class=None):

        self.hostname = hostname
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen() #configure the socket to the listen mode
        
        self.client = None
        self.request = None
        self.parser = None
        self.url = None
        self.headers = None


        self.request_class = request_class or Request ##request class to use for creatign request object
        self.request_handler = request_handler

        
    def run(self):
        while True:
            #wait for the client to connect to the server
            client, addr = self.socket.accept()
            print('Got connection from {}'.format(str(addr)))

            #assign the client
            self.client = client
            self.handle_client()

        
    def on_url(self, url):
        #print(url)
        self.url = url

    def on_message_begin(self):
        pass
        
    
    def on_header(self, name, value):
        self.headers.append((name.decode().casefold(), value.decode()))

    
    def on_headers_complete(self):
        self.request = self.request_class(
            url_bytes = self.url,
            method = self.parser.get_method().decode(),
            client = self.client,
            headers = CIDict(self.headers),
            version = self.parser.get_http_version()

        )
        
        

    def on_body(self, body):
        self.request.append(body)
    
    def on_message_complete(self):
        self.request.body = b''.join(self.request.body)
        #now call the request handler and pass all the reqqust
        self.request_handler(
            self.request,
            self.write_response)
        
    def write_response(self, response):
        try:
            self.client.send(response.output())
        except Exception as e:
            log.error('Failed to write the response')
        finally:
            self.clean_up()

            

    def handle_client(self):
        #wait for the message to arrive
        if self.parser is None:
            self.headers = []
            self.parser = HttpRequestParser(self)

        
        msg = self.client.recv(1000)
        self.parser.feed_data(msg)
        

        #self.client.send(msg)
        #create a parser if this is first time
        #self.clean_up()
    
    def clean_up(self):
        self.parser = None
        self.request = None
        self.url = None
        self.headers = None

        #now assume the keep-alive is False
        self.client.close()
        self.client  = None

def main():
    parser = argparse.ArgumentParser(description='A http server')
    parser.add_argument('--host', dest='host', type=str, default='localhost')
    parser.add_argument('--port', dest='port', type=int, default=8000)

    args = parser.parse_args()
    server = Server(args.host, args.port)
    #run the serer
    server.run()


if __name__ == '__main__':
    main()



        