"""
FinancialModelingPrep API Calls
"""

import matplotlib


# Allows matplotlib to draw files that are in memory (all plt objects)
matplotlib.use("Agg")

import os
from django.shortcuts import render, redirect
from .forms import StockForm
from .models import StockSearch
import requests
import matplotlib.pyplot as plt
from django.conf import settings
import json


def fetch_stock_price(ticker: str) -> json:
    """ """
    url = f"https://financialmodelingprep.com/stable/quote?symbol={ticker}&apikey={settings.FMP_API_KEY}"
    r = requests.get(url).json()
    if not r:
        return None
    return r[0].get("price", None)


def fetch_stock_data(ticker: str) -> json:
    """ """
    url = f"https://financialmodelingprep.com/stable/quote?symbol={ticker}&apikey={settings.FMP_API_KEY}"
    r = requests.get(url).json()
    if not r:
        return {None}
    return {"name": r[0].get("name", None), "price": r[0].get("price", None)}


def fetch_stock_history(ticker: str) -> dict:
    """
    Docstring for fetch_stock_history

    :param ticker: Description
    :type ticker: str
    """
    # TODO - from, to options?
    url = f"https://financialmodelingprep.com/stable/historical-price-eod/full?symbol={ticker}&apikey={settings.FMP_API_KEY}"
    r = requests.get(url).json()
    # Dates/prices in reverse order to show time progression
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
    return res


def home(request):
    history = StockSearch.objects.all()
    chart_path = ""
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data["ticker"].upper()

            name_and_price = fetch_stock_data(ticker)

            if not any(name_and_price):
                return render(
                    request,
                    "index.html",
                    {
                        "form": form,
                        "error": f"No data found for ticker '{ticker}'",
                        "charts": chart_path,
                        "history": history,
                    },
                )

            StockSearch.objects.create(
                ticker=ticker,
                name=name_and_price["name"],
                fetched_price=name_and_price["price"],
            )

            data = fetch_stock_history(ticker)
            if data:
                chart_path = make_charts(data, ticker)

            return render(
                    request,
                    "index.html",
                    {
                        "form": form,
                        "charts": chart_path,
                        "history": history,
                    },
                        )

    else:
        form = StockForm()

    return render(
        request,
        "index.html",
        {
            "form": form,
            "charts": chart_path,
            "history": history,
        },
    )


def make_charts(data: dict, ticker: str) -> str:
    """
    Make Charts for ticker, save static

    :param data: Description
    :type data: dict
    :param ticker: Description
    :type ticker: str
    """
    data = fetch_stock_history(ticker)
    if data:
        prices, dates = data["prices"], data["dates"]

        plt.figure(figsize=(8, 4))
        plt.plot(dates, prices)
        plt.title(f"{ticker} — 1 Year Price")
        plt.xticks(ticks=dates[0::45], rotation=45)
        plt.grid(True)
        plt.ylabel("Closing Price (USD)")
        plt.xlabel("Closing Date")
        plt.tight_layout()
        # Static dir
        filename = f"{ticker}.png"
        fpath = os.path.join(settings.MEDIA_ROOT, filename)
        plt.savefig(fpath)
        plt.close()
        return fpath


def clear_history(request):
    StockSearch.objects.all().delete()
    return redirect("/")
