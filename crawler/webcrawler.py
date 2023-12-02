from bs4 import BeautifulSoup
from requests import Session, RequestException

URL = "https://www.pro-football-reference.com"
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


def main():
    http_session = Session()
    html = request_url(session=http_session, url=URL)
    soup = parse_html_to_soup(html)

    print(soup)


if __name__ == "__main__":
    main()
