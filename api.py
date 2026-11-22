from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from gve.models import Trade
from gve.analytics.footprint import build_footprint
from gve.analytics.delta import calculate_delta, calculate_cvd
from gve.analytics.profile import build_volume_profile
from decimal import Decimal
from datetime import datetime, timezone
import os

app = FastAPI(title="GVE Order Flow API", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
                   allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])

class TradeIn(BaseModel):
    timestamp_ns: int
    price: Decimal = Field(gt=0)
    size: Decimal = Field(ge=0)
    side: str
    symbol: str = "GC"
    provider: str = "unknown"
    dataset: str = "unknown"
    quality: str = "UNVERIFIED"

class AnalyticsRequest(BaseModel):
    trades: list[TradeIn]
    tick_size: Decimal = Field(default=Decimal("0.1"), gt=0)
    value_area_pct: Decimal = Field(default=Decimal("70"), ge=50, le=90)

def _trades(items):
    out=[]
    for x in items:
        side=x.side.upper()
        if side not in ("BUY","SELL","UNKNOWN"):
            raise ValueError("side must be BUY, SELL or UNKNOWN")
        out.append(Trade(timestamp_ns=x.timestamp_ns, price=x.price, size=x.size,
                         side=side, symbol=x.symbol, provider=x.provider,
                         dataset=x.dataset, quality=x.quality))
    return out

@app.get("/api/health")
def health():
    return {"service":"gve-orderflow-api","version":"0.2.0","status":"ok",
            "live_trading_enabled":False,"auto_execution_enabled":False}

@app.get("/api/data/status")
def data_status():
    return {"databento_configured":bool(os.getenv("DATABENTO_API_KEY")),
            "twelvedata_configured":bool(os.getenv("TWELVEDATA_API_KEY")),
            "data_mode":os.getenv("DATA_MODE","historical"),
            "live_trading_enabled":False,"auto_execution_enabled":False,
            "market_data_validated":False,
            "decision":"DATA INVALID — NO TRADE"}

@app.post("/api/orderflow/analyze")
def analyze(request: AnalyticsRequest):
    trades=_trades(request.trades)
    fp=build_footprint(trades, request.tick_size)
    delta=calculate_delta(trades)
    cvd=calculate_cvd(trades)
    profile=build_volume_profile(trades, request.tick_size, request.value_area_pct)
    # API demo endpoint intentionally does not confer source authenticity or trade permission.
    return {"source_quality":"UNVERIFIED_INPUT","decision":"DATA INVALID — NO TRADE",
            "footprint":[{k:str(v) if isinstance(v,Decimal) else v for k,v in row.items()} for row in fp],
            "delta":{k:str(v) if isinstance(v,Decimal) else v for k,v in delta.items()},
            "cvd":[{k:str(v) if isinstance(v,Decimal) else v for k,v in row.items()} for row in cvd],
            "volume_profile":{k:([{kk:str(vv) if isinstance(vv,Decimal) else vv for kk,vv in x.items()} for x in v] if k=="levels" else str(v) if isinstance(v,Decimal) else v) for k,v in profile.items()}}
