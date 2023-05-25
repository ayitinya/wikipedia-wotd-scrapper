from http.server import BaseHTTPRequestHandler


import json
from datetime import datetime


from bs4 import BeautifulSoup
import requests


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

    URL: str = "https://en.wiktionary.org/wiki/Wiktionary:Word_of_the_day"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="WOTD-rss-title")
    date = soup.find(id="WOTD-rss-date")

    if results is not None and date is not None:
        month = MONTHS[date.text.split(" ")[0]]
        day = date.text.split(" ")[1].replace(",", "")

        try:
            month = int(month)
            day = int(day)
        except ValueError:
            raise ValueError("Month or day is not an integer")

        print(f"{month}-{day}")
        
        word_details = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{results.text}")
        if word_details.status_code == 200:
            return json.dumps({"wotd": results.text, "timestamp": datetime(year=datetime.now().year, month=month, day=day).isoformat(), "details": word_details.json()[0]})
        json_data = json.dumps(
            {"wotd": results.text, "timestamp": datetime(year=datetime.now().year, month=month, day=day).isoformat()})
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
