from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Type


import json
from datetime import datetime


from bs4 import BeautifulSoup
import requests


def run(handler_class: Type[BaseHTTPRequestHandler], server_class: Type[HTTPServer] = HTTPServer):
    server_address = ('', 8000)
    httpd = server_class(server_address=server_address,
                         RequestHandlerClass=handler_class)
    httpd.serve_forever()


def get_wotd():
    MONTHS = {
        "January": "01",
        "February": "02",
        "March": "03",
        "April": "04",
        "May": "05",
        "June": "06",
        "July": "07",
        "August": "08",
        "September": "09",
        "October": "10",
        "November": "11",
        "December": "12"
    }

    URL: str = "https://en.wiktionary.org/w/api.php?action=featuredfeed&feed=wotd&feedformat=atom"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "xml")

    entries = soup.find_all("summary")
    if len(entries) != 0:
        entry = entries[-1]

        parsed_entry = BeautifulSoup(entry.text, "html.parser")
        print(parsed_entry)

        results = parsed_entry.find(id="WOTD-rss-title")
        date = parsed_entry.find(id="WOTD-rss-date")

        if results is not None and date is not None:
            month = MONTHS[date.text.split(" ")[0]]
            day = date.text.split(" ")[1].replace(",", "")

            try:
                month = int(month)
                day = int(day)
            except ValueError:
                raise ValueError("Month or day is not an integer")

            print(f"{month}-{day}")

            json_data = json.dumps(
                {"wotd": results.text, "timestamp": datetime(year=datetime.now().year, month=month, day=day).isoformat()})
            return json_data
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
    run(handler)
