from http.server import BaseHTTPRequestHandler

from get_wotd import get_wotd

import json
from typing import Dict
from datetime import datetime


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
