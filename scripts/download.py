import yfinance as yf
import csv
from tqdm import tqdm
from pmaso.utils import *
import time

def main():
    print("yfinance verson:",yf.__version__)
    TICKER_FILE = "./assets/tickers.csv"
    ticker_rows = load_csv(TICKER_FILE)
    tickers = load_tickers(ticker_rows)

    for ticker in tqdm(tickers,desc="Downloading Tickers..."):
        dat = yf.Ticker(ticker)
        hist = dat.history(period="10y", interval="1mo")
        path = f"./exports/{ticker}.csv"
        hist.to_csv(path)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
