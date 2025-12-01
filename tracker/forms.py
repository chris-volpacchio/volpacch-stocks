from django import forms

class StockForm(forms.Form):
    ticker = forms.CharField(
        label="Enter Ticker",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "e.g. AAPL, TSLA, BTCUSD"})
    )
