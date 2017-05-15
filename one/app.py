import os
import sys
from one.server import Server
from one.response import HTTPResponse



class Robus:

    def __init__(self, name):
        self.name = name
        self.router = {}
        self.is_running = False

    def route(self, uri, methods=frozenset({'GET'})):
        ''' Decorator function that registers views to the router'''
        def response(handler):

            self.router[uri] = handler
            return handler
        
        return response
    
    def run(self, hostname='localhost', port=12000):
        server = Server(hostname, port, self.handle_request)
        server.run()
        
    
    def handle_request(self, request, write_callback):
        #place the request to the current context
        request.app = self
        #fetch hadnler from the router
        handler = self.router.get(request.path)
        print(request.path)
        if handler is None:
            write_callback(HTTPResponse(''))
            return
        #run the response handler
        response = handler(request)
        #finallt wruite the resonse
        write_callback(response)

    