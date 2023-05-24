from http.server import BaseHTTPRequestHandler


import json
from datetime import datetime


from bs4 import BeautifulSoup
import requests


def get_wotd():
    URL: str = "https://en.wiktionary.org/wiki/Wiktionary:Word_of_the_day"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="WOTD-rss-title")

    if results is not None:
        json_data = json.dumps(
            {"wotd": results.text, "timestamp": datetime.now().isoformat()})
        return json_data
    else:
        return None


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        json_data = get_wotd()
        if json_data is not None:

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
            return
        else:
            self.send_response(404)
            return


if __name__ == "__main__":
    print(get_wotd())
