from django.template import Library
from forex_python.converter import CurrencyRates

register = Library()


def usd(eur: str):
    xr = float(CurrencyRates().get_rate("EUR", "USD"))
    usd = float(eur) * xr
    return format(usd, ".2f")  # round(usd, 2)


register.filter("usd", usd)
