from bs4 import BeautifulSoup
from requests import Session, RequestException

URL = "https://www.pro-football-reference.com"
BOX_URL = URL + "/boxscores/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}


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


def main():
    http_session = Session()
    html = request_url(session=http_session, url=BOX_URL)
    soup = parse_html_to_soup(html)

    key = extract_current_week_info(soup=soup)
    boxscore_links = extract_boxscore_links(soup=soup)
    print(boxscore_links)


if __name__ == "__main__":
    main()
