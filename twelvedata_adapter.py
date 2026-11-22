"""Twelve Data spot reference adapter; never presents spot OHLC as exchange order flow."""
import os
import urllib.parse
import urllib.request
import json

class TwelveDataAdapter:
    BASE = "https://api.twelvedata.com/time_series"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TWELVEDATA_API_KEY")
        if not self.api_key:
            raise RuntimeError("TWELVEDATA_API_KEY is not configured")

    def fetch_ohlc(self, *, symbol: str = "XAU/USD", interval: str = "5min",
                   outputsize: int = 100):
        params = urllib.parse.urlencode({
            "symbol": symbol, "interval": interval,
            "outputsize": outputsize, "apikey": self.api_key
        })
        request = urllib.request.Request(self.BASE + "?" + params,
                                         headers={"Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if "values" not in payload:
            raise RuntimeError(f"Twelve Data returned an error: {payload.get('message', 'unknown')}")
        return payload
