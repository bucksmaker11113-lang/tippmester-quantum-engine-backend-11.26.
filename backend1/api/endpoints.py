# ============================================================
# API ENDPOINTOK – STRATÉGIA, TIPPEK, BANKROLL, CHAT
# Full upgrade version – odds feed + workers kompatibilis
# ============================================================

from fastapi import APIRouter
from core.strategy_engine import StrategyEngine
from api.push_api import send_push_to_all

# ------------------------------------------------------------
# Alap bankrollok – ezeket később configból is olvashatjuk
# ------------------------------------------------------------
strategy = StrategyEngine(
    initial_single=1000,
    initial_kombi=300,
    initial_live=200
)

router = APIRouter()

# Ideiglenes chat store – később Redis-re cserélhető
chat_history_store = []


# ============================================================
# 1) SINGLE TIPPEK
# ============================================================
@router.get("/single")
async def get_single():
    """
    Single tippek lekérése a stratégia engine alapján.
    A valós odds feed integrációval automatikusan frissek lesznek.
    """
    all_events = []          # majd odds feed tölti be
    live_events = []         # future use
    picks = strategy.generate_daily_picks(all_events, live_events)
    return picks["single"]


# ============================================================
# 2) KOMBI TIPPEK
# ============================================================
@router.get("/kombi")
async def get_kombi():
    """
    Egy kombi szelvény (4–5 esemény) + kiszámolt tét.
    """
    all_events = []
    live_events = []
    picks = strategy.generate_daily_picks(all_events, live_events)
    return {
        "events": picks["kombi"],
        "stake": picks["kombi_stake"]
    }


# ============================================================
# 3) LIVE TIPPEK
# ============================================================
@router.get("/live")
async def get_live():
    """
    Az élő tippek listája.
    A valós idejű websocket stream is használja, de az API is visszaadja.
    """
    all_events = []
    live_events = []
    picks = strategy.generate_daily_picks(all_events, live_events)
    return picks["live"]


# ============================================================
# 4) BANKROLL
# ============================================================
@router.get("/bankroll")
async def get_bankroll():
    """
    A 3 külön bankroll visszaadása a frontend HUD számára.
    """
    return {
        "single_bankroll": strategy.single_bankroll,
        "kombi_bankroll": strategy.kombi_bankroll,
        "live_bankroll": strategy.live_bankroll,
    }


# ============================================================
# 5) CHAT – ELŐZMÉNYEK
# ============================================================
@router.get("/chat/history")
async def chat_history():
    """
    Chat üzenetek története – később Redis-be kerül.
    """
    return chat_history_store


# ============================================================
# 6) CHAT – ÜZENET KÜLDÉSE
# ============================================================
@router.post("/chat/send")
async def chat_send(item: dict):
    """
    Chat üzenet küldése.
    Websocket + push értesítés kompatibilis.
    """
    message = {
        "text": item.get("text", ""),
        "sender": "user"
    }

    chat_history_store.append(message)

    # opcionális: push küldése minden feliratkozónak
    try:
        send_push_to_all({
            "message": message["text"],
            "sender": message["sender"]
        })
    except:
        pass

    return {"status": "ok", "message": message}
