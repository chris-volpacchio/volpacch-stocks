import matplotlib

matplotlib.use("Agg")

import os
import requests
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf


def test_fetch_stock_price(ticker):
    url = f"https://financialmodelingprep.com/stable/quote?symbol={ticker}&apikey={os.getenv("FMP_API_KEY", "demo")}"
    # url = "https://financialmodelingprep.com/stable/search-symbol?query=AAPL&apikey=5bTgfLszHerVR4vRYXBAVMz1Lm5oVequ"
    r = requests.get(url).json()
    # TODO - expected return empty object or NoneType?
    if not r:
        return None
    print(r)
    print(r[0].get("price", None))


def test_fetch_stock_history(ticker: str) -> dict:
    """

    Docstring for fetch_stock_history

    :param ticker: Description
    :type ticker: str
    """
    # from, to
    url = f"https://financialmodelingprep.com/stable/historical-price-eod/full?symbol={ticker}&apikey={os.getenv("FMP_API_KEY", "demo")}"
    # url =   "https://financialmodelingprep.com/stable/historical-price-eod/full?symbol=AAPL&apikey=5bTgfLszHerVR4vRYXBAVMz1Lm5oVequ"
    r = requests.get(url).json()
    print(f"{r[0].keys()=}")
    # print(len(r))
    # if not r or "historical" not in r:
    #     print("Missing historical")
    #     return None
    # histor = r["historical"]
    # assert histor
    # print([x["close"] for x in r])
    res = {
        "prices": [x["close"] for x in r][::-1],
        "dates": [x["date"] for x in r][::-1],
    }
    candlestick_keys = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    _dict = {key: [x[key] for x in r][::-1] for key in candlestick_keys}
    res.update(_dict)
    print(f"{res.keys()=}")
    # print(res)
    return res
    # print({
    #     "prices": [x["close"] for x in histor][::-1],
    #     "dates": [x["date"] for x in histor][::-1]
    # })


def test_make_charts(ticker: str):
    data = test_fetch_stock_history(ticker)
    print(data)
    if data:
        print(data)
        prices = data["prices"]
        dates = data["dates"]
        plt.figure(figsize=(8, 4))
        plt.plot(dates, prices)
        plt.title(f"{ticker} — 1 Year Price")
        plt.xticks(ticks=dates[0::45], rotation=45)
        plt.grid(True)
        plt.ylabel("Closing Price (USD)")
        plt.xlabel("Closing Date")
        plt.tight_layout()
        plt.show()
        # chart_path = f"static/charts/{ticker}.png"
        # BASE_DIR = os.path.abspath(
        #     os.path.join(
        #         os.path.dirname(os.path.abspath(__file__)),
        #         "../../",
        #         f"static/charts/{ticker}.png",
        #     )
        # )
        # print(f"{BASE_DIR=}")
        # plt.savefig(chart_path)
        # plt.close()


def test_make_candlestick_chart_static(ticker):
    data = test_fetch_stock_history(ticker)
    # print(data)
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    mpf.plot(
        df,
        type="candle",
        style="yahoo",
        title=f"{ticker} Candlestick Chart",
        volume=True,
    )


if __name__ == "__main__":
    load_dotenv()
    # test_fetch_stock_price("AAPL")
    # test_fetch_stock_history("AAPL")
    test_make_charts("AAPL")
