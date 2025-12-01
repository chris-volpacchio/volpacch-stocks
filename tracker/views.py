from django.shortcuts import render, redirect
from .forms import StockForm
from .models import StockSearch
import requests
import matplotlib.pyplot as plt
import os
from django.conf import settings

def fetch_stock_price(ticker):
    url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={settings.FMP_API_KEY}"
    r = requests.get(url).json()
    if not r:
        return None
    return r[0].get("price", None)

def fetch_stock_history(ticker):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?timeseries=365&apikey={settings.FMP_API_KEY}"
    r = requests.get(url).json()
    if not r or "historical" not in r:
        return None
    histor = r["historical"]
    return {
        "prices": [x["close"] for x in histor][::-1],
        "dates": [x["date"] for x in histor][::-1]
    }

def home(request):
    charts = []
    history = StockSearch.objects.all()

    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data["ticker"].upper()

            price = fetch_stock_price(ticker)
            if price is None:
                return render(request, "index.html", {
                    "form": form,
                    "error": f"No data found for ticker '{ticker}'",
                    "charts": charts,
                    "history": history,
                })

            StockSearch.objects.create(
                ticker=ticker,
                fetched_price=price
            )

            data = fetch_stock_history(ticker)
            if data:
                prices = data["prices"]
                dates = data["dates"]

                plt.figure(figsize=(8,4))
                plt.plot(dates, prices)
                plt.title(f"{ticker} — 1 Year Price")
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()

                chart_path = f"static/charts/{ticker}.png"
                plt.savefig(chart_path)
                plt.close()

                charts.append("/" + chart_path)

            return redirect("/")

    else:
        form = StockForm()

    return render(request, "index.html", {
        "form": form,
        "charts": charts,
        "history": history,
    })

def clear_history(request):
    StockSearch.objects.all().delete()
    return redirect("/")
