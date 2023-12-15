import json
import time
from bs4 import BeautifulSoup
from requests import Session, RequestException
from rich import print

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}
INPUT_PATH = "/home/brandon/Workspace/MyFirstApp/season_links.json"


def read_json(path: str) -> dict:
    with open(path, "r") as file:
        data = json.load(file)
    return data


def request_url(session: Session, url: str, retries: int = 3, timeout: int = 10):
    for _ in range(retries):
        try:
            response = session.get(url=url, timeout=timeout, headers=HEADERS)
            response.raise_for_status()

            return response.text

        except RequestException as raised_exception:
            print(f"Die Anfrage an {url} ist fehlgeschlagen.")
            continue
    print(f"Die Anfrage an {url} ist final fehlgeschlagen.")
    return


def parse_html_to_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def main():
    boxscore_links = read_json(path=INPUT_PATH)
    http_session = Session()

    # url = "https://www.pro-football-reference.com/boxscores/202309110nyj.htm"

    scraped_data = dict()

    for key, urls in boxscore_links.items():
        payload_data = list()
        for url in urls:
            time.sleep(2)
            html = request_url(session=http_session, url=url)
            soup = parse_html_to_soup(html)
            table = soup.find("table", class_="linescore")

            rows = table.select("table tbody tr")

            teams = []
            for row in rows:
                table_data_cells = row.find_all(["td"])
                team_name = table_data_cells[1].text
                point_cells = table_data_cells[2:]
                points = [int(cell.text) for cell in point_cells]
                final_points = points[-1]
                quarter_points = points[:-1]
                if not (final_points == sum(quarter_points)):
                    raise ValueError("Quarter Points do not match final points")

                result = (team_name, final_points)
                teams.append(result)

            data = {
                "team": teams[1][0],
                "opponent": teams[0][0],
                "points_scored": teams[1][1],
                "points_allowed": teams[0][1],
            }

            payload_data.append(data)
            print(key)
            print(payload_data)
        scraped_data[key] = payload_data
    return


if __name__ == "__main__":
    main()
