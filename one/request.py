import os
import sys
from httptools import parse_url

class Request:

    def __init__(self, url_bytes, method, version, headers, client ):
        self._parsed_url = parse_url(url_bytes)
        self.app = None
        
        self.headers = headers
        self.method = method
        self.client = client
        self.version = version

        self.body = []
    
    @property
    def path(self):
        return self._parsed_url.path.decode('utf-8')
