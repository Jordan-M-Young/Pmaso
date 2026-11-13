"""Fetch the NYSE listings directory (equities, ETFs, indices, REITs) via its quotes filter API."""

import csv
import time
import requests

BASE_URL = "https://www.nyse.com"
LISTINGS_PAGE = f"{BASE_URL}/listings_directory/stock"
FILTER_URL = f"{BASE_URL}/api/quotes/filter"
INSTRUMENT_TYPES = ["EQUITY", "EXCHANGE_TRADED_FUND", "INDEX", "REIT"]
OUTPUT = "./assets/tickers.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:157.0) "
        "Gecko/20100101 Firefox/157.0"
    ),
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": LISTINGS_PAGE,
    "Origin": BASE_URL,
}


def make_session() -> requests.Session:
    """Create a session and visit the listings page so the server sets fresh cookies."""
    session = requests.Session()
    session.headers.update(HEADERS)
    session.get(LISTINGS_PAGE, timeout=30)
    return session

def fetch_page(
    session: requests.Session,
    page_number: int,
    page_size: int = 10,
    instrument_type: str = "EQUITY",
) -> list[dict]:
    payload = {
        "instrumentType": instrument_type,
        "pageNumber": page_number,
        "sortColumn": "NORMALIZED_TICKER",
        "sortOrder": "ASC",
        "maxResultsPerPage": page_size,
        "filterToken": "",
    }
    resp = session.post(FILTER_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()




def fetch_type(
    session: requests.Session,
    instrument_type: str,
    page_size: int = 1000,
    delay: float = 0.5,
) -> list[dict]:
    """Page through the API until every listing of one instrument type is fetched."""
    results: list[dict] = []
    page = 1
    while True:
        rows = fetch_page(session, page, page_size, instrument_type=instrument_type)
        if not rows:
            break
        results.extend(rows)
        # "total" is the count for this instrument type only
        total = rows[0].get("total", len(results))
        print(f"{instrument_type} page {page}: {len(results)}/{total}")
        if len(results) >= total or len(rows) < page_size:
            break
        page += 1
        time.sleep(delay)
    return results


def fetch_all(instrument_types: list[str] = INSTRUMENT_TYPES) -> list[dict]:
    """Fetch every instrument type, tagging each row with its type.

    A listing can appear under more than one type (e.g. REITs also show up
    as EQUITY); the later, more specific type wins.
    """
    session = make_session()
    by_key: dict[tuple[str, str], dict] = {}
    for instrument_type in instrument_types:
        for row in fetch_type(session, instrument_type):
            row["instrumentType"] = instrument_type
            by_key[(row["normalizedTicker"], row.get("url", ""))] = row
    return sorted(by_key.values(), key=lambda r: r["normalizedTicker"])


def market_code(url: str) -> str:
    """Pull the MIC out of a quote URL.

    .../quote/XNYS:AA      -> XNYS
    .../quote/index/ABCERI -> "" (indices have no listing market)
    """
    last = url.rsplit("/", 1)[-1]
    return last.split(":", 1)[0] if ":" in last else ""


def save_csv(rows: list[dict], path: str) -> None:
    """Write ticker, name, market (MIC) and instrument type to CSV."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ticker", "name", "mic", "type"])
        for row in rows:
            writer.writerow([
                row["normalizedTicker"],
                row["instrumentName"],
                market_code(row.get("url", "")),
                row["instrumentType"],
            ])


def main():
    rows = fetch_all()
    save_csv(rows, OUTPUT)
    print(f"wrote {len(rows)} tickers to {OUTPUT}")


if __name__ == "__main__":
    main()
