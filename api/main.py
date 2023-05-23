from http.server import BaseHTTPRequestHandler

from get_wotd import get_wotd

import json
from typing import Dict
from datetime import datetime


from bs4 import BeautifulSoup
import requests

def get_wotd():
    URL: str = "https://en.wiktionary.org/wiki/Wiktionary:Word_of_the_day"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="WOTD-rss-title")

    if results is not None:
        json_data = json.dumps({"wotd": results.text, "timestamp": str(datetime.now())})
        with open("wotd.json", "w") as f:
            f.write(json_data)
        return json_data
    else:
        return None

class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        try:
            with open("wotd.json", "r") as f:
                json_data = f.read()
                
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                
                parse_json: Dict[str, str]  = json.loads(json_data)
                current_time = datetime.now()

                delta = current_time - datetime.strptime(parse_json["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
                
                if delta.days > 0:
                    json_data = get_wotd()
                    if json_data is not None:
                        
                        self.wfile.write(json_data.encode('utf-8'))
                        return
                else:
                    self.wfile.write(json_data.encode('utf-8'))
                    return
                    
                    
        except FileNotFoundError:
            json_data = get_wotd()
            if json_data is not None:
                
                self.send_response(200)
                self.send_header('Content-type','application/json')
                self.end_headers()
                self.wfile.write(json_data.encode('utf-8'))
                return
            else:
                self.send_response(404)
                return
        except:
            self.send_response(500)
            return
