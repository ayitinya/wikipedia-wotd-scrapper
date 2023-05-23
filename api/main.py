from http.server import BaseHTTPRequestHandler

from bs4 import BeautifulSoup
import requests
import json


class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        
        try:
            URL: str = "https://en.wiktionary.org/wiki/Wiktionary:Word_of_the_day"
            page = requests.get(URL)

            soup = BeautifulSoup(page.content, "html.parser")

            results = soup.find(id="WOTD-rss-title")

            if results is not None:
                json_data = json.dumps({"wotd": results.text})
            
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.send_response(code=200, message=json_data)
                self.wfile.write('Hello, world!'.encode('utf-8'))
                return
                
            else:
                self.send_response(404)
                return
        except:
            self.send_response(500)
            return