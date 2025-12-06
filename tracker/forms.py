"""
Create Form entries for Page
"""

from django import forms


class StockForm(forms.Form):
    ticker = forms.CharField(
        label="Enter Ticker",
        max_length=20,
        widget=forms.TextInput(
            attrs={"placeholder": "ENTER STOCK TICKER HERE e.g. AAPL, TSLA", "size": 50}
        ),
    )


# TODO - have start and end date for charts
