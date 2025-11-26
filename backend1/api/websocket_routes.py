# ============================================================
# WEBSOCKET ROUTES – LIVE TIP STREAM + CHAT STREAM
# Full upgrade version (stable, scalable)
# ============================================================

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ws_router = APIRouter()

# ------------------------------------------------------------
# KLIENS LISTÁK
# ------------------------------------------------------------
live_clients = []
chat_clients = []


# ============================================================
# 1) LIVE TIPPEK WEBSOCKET
# ============================================================
@ws_router.websocket("/ws/live")
async def live_websocket(ws: WebSocket):
    await ws.accept()
    live_clients.append(ws)

    try:
        while True:
            # a live ws kliensek nem küldenek adatot, csak kapnak
            await ws.receive_text()
    except WebSocketDisconnect:
        if ws in live_clients:
            live_clients.remove(ws)
    except:
        try:
            live_clients.remove(ws)
        except:
            pass


# ------------------------------------------------------------
# LIVE TIPP KÜLDÉSE MINDEN KLIENSNEK
# ------------------------------------------------------------
async def broadcast_live_tips(tips: list):
    """
    Live tippek kiküldése az összes élő websocket kliensnek.

    Formátum:
    {
        "type": "live",
        "tips": [...]
    }
    """
    dead = []
    for client in live_clients:
        try:
            await client.send_json({
                "type": "live",
                "tips": tips
            })
        except:
            dead.append(client)

    # halott kliensek tisztítása
    for dc in dead:
        if dc in live_clients:
            live_clients.remove(dc)


# ============================================================
# 2) CHAT WEBSOCKET
# ============================================================
@ws_router.websocket("/ws/chat")
async def chat_websocket(ws: WebSocket):
    await ws.accept()
    chat_clients.append(ws)

    try:
        while True:
            # üzenet fogadása
            msg = await ws.receive_text()

            # továbbküldés minden kliensnek
            await broadcast_chat_message(msg)

    except WebSocketDisconnect:
        if ws in chat_clients:
            chat_clients.remove(ws)
    except:
        try:
            chat_clients.remove(ws)
        except:
            pass


# ------------------------------------------------------------
# CHAT ÜZENET SZÓRÁSA
# ------------------------------------------------------------
async def broadcast_chat_message(text: str):
    """
    Chat üzenet kiküldése minden websocket kliensnek.

    Formátum:
    {
        "type": "chat",
        "message": "szöveg"
    }
    """
    dead = []
    for client in chat_clients:
        try:
            await client.send_json({
                "type": "chat",
                "message": text
            })
        except:
            dead.append(client)

    # halott kliensek eltávolítása
    for dc in dead:
        if dc in chat_clients:
            chat_clients.remove(dc)
