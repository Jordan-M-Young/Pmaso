import streamlit as st
import pmaso.utils as utils

TICKER_FILE="./assets/tickers.csv"
TICKER_DATA = utils.load_csv(TICKER_FILE)
TICKERS = utils.load_tickers(TICKER_DATA)


def main():
    option = st.selectbox(
        'Select a ticker.',
        TICKERS)



if __name__ == "__main__":
    main()
