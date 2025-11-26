# ============================================================
# FastAPI Endpointok – Frontend + Mobil app számára
# ============================================================

from fastapi import FastAPI
from backend.core.strategy_engine import StrategyEngine

app = FastAPI()

strategy = StrategyEngine(1000, 300, 200)


@app.get("/api/single")
def get_single():
    return {"single": "placeholder – strategy_engine integrálható ide"}


@app.get("/api/kombi")
def get_kombi():
    return {"kombi": "placeholder"}


@app.get("/api/live")
def get_live():
    return {"live": "placeholder"}
