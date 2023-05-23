from http.server import BaseHTTPRequestHandler

from get_wotd import get_wotd


class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        try:
            with open("wotd.json", "r") as f:
                json_data = f.read()
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
