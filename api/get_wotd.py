from bs4 import BeautifulSoup
import requests
import json
import datetime

def get_wotd():
    URL: str = "https://en.wiktionary.org/wiki/Wiktionary:Word_of_the_day"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="WOTD-rss-title")

    if results is not None:
        json_data = json.dumps({"wotd": results.text, "timestamp": str(datetime.datetime.now())})
        with open("wotd.json", "w") as f:
            f.write(json_data)
        return json_data
    else:
        return None


if __name__ == "__main__":
    get_wotd()