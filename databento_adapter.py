"""Databento adapter boundary. Optional SDK import; credentials stay server-side."""
import os

class DatabentoAdapter:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("DATABENTO_API_KEY")
        if not self.api_key:
            raise RuntimeError("DATABENTO_API_KEY is not configured")
        try:
            import databento as db
        except ImportError as exc:
            raise RuntimeError("Install the optional 'databento' SDK before connecting") from exc
        self._db = db

    def historical_client(self):
        return self._db.Historical(self.api_key)

    def fetch_trades(self, *, start: str, end: str, symbol: str = "GC.FUT",
                     dataset: str = "GLBX.MDP3"):
        """Fetch raw Databento trade records. Validate schema/metadata before analytics."""
        client = self.historical_client()
        return client.timeseries.get_range(
            dataset=dataset, symbols=[symbol], stype_in="parent",
            schema="trades", start=start, end=end
        )
