from django.db import models

class StockSearch(models.Model):
    ticker = models.CharField(max_length=20)
    fetched_price = models.FloatField()
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-searched_at"]

    def __str__(self):
        return f"{self.ticker} — {self.fetched_price}"
