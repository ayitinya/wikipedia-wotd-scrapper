from http.server import BaseHTTPRequestHandler

from get_wotd import get_wotd


class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        get_wotd()
