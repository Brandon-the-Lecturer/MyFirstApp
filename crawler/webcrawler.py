import json

from bs4 import BeautifulSoup
from requests import Session, RequestException

from rich import print

URL = "https://www.pro-football-reference.com"
BOX_URL = URL + "/boxscores/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}
OUTPUT_FILE = "season_links.json"


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


def extract_current_week_info(soup: BeautifulSoup) -> list:
    h2_element = soup.select_one("h2").text
    info_list = h2_element.split()
    return "/".join(info_list)


def extract_boxscore_links(soup: BeautifulSoup) -> list:
    links = soup.select("a:-soup-contains('Final')")
    return [URL + link["href"] for link in links]


def create_week_links(key: str) -> list:
    season, _, current_week_no = key.split("/")
    week_links = list()

    for week_no in range(int(current_week_no), 0, -1):
        week_link = f"{URL}/years/{season}/week_{week_no}.htm"
        week_links.append(week_link)
    return week_links


def transform_to_season_boxscore_links(session: Session, week_links: list) -> dict:
    season_boxscore_links = dict()

    for week_link in week_links:
        week_key = "/".join(week_link.split(".")[2].split("/")[-2:])
        html = request_url(session=session, url=week_link)
        soup = parse_html_to_soup(html=html)
        boxscore_links = extract_boxscore_links(soup=soup)
        season_boxscore_links[week_key] = boxscore_links
    return season_boxscore_links


def load_to_json_file(path: str, data: dict) -> None:
    with open(path, "w") as file:
        json.dump(data, file)
    return


def main():
    http_session = Session()

    html = request_url(session=http_session, url=BOX_URL)
    soup = parse_html_to_soup(html)
    key = extract_current_week_info(soup=soup)
    week_links = create_week_links(key)

    season_boxscore_links = transform_to_season_boxscore_links(
        session=http_session, week_links=week_links
    )

    load_to_json_file(path=OUTPUT_FILE, data=season_boxscore_links)


if __name__ == "__main__":
    main()
