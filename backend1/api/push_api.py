# ============================================================
# PUSH API – LIVE TIP ÉRTESÍTÉSEKHEZ
# WebPush (VAPID) + FastAPI backend
# ============================================================

import json
import os
from fastapi import APIRouter
from pywebpush import webpush, WebPushException

router = APIRouter()

# ------------------------------------------------------------
# VAPID KULCSOK (EZEKET A HETZNEREN FOGOD GENERÁLNI)
# ------------------------------------------------------------
VAPID_PUBLIC_KEY = "PUT_YOUR_PUBLIC_KEY_HERE"
VAPID_PRIVATE_KEY = "PUT_YOUR_PRIVATE_KEY_HERE"
VAPID_EMAIL = "mailto:admin@tippmester.hu"

# ------------------------------------------------------------
# Feliratkozók tárolása — később Redis is lehet
# ------------------------------------------------------------
SUBSCRIBERS_FILE = "subscribers.json"


def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        try:
            return json.load(open(SUBSCRIBERS_FILE, "r"))
        except:
            return []
    return []


def save_subscribers(subs):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(subs, f, indent=2)


# ============================================================
# FELIRATKOZÁS (frontend push.js hívja)
# ============================================================
@router.post("/push/subscribe")
async def subscribe(subscription: dict):
    subs = load_subscribers()

    # ha már létezik, ne írjuk duplán
    if subscription not in subs:
        subs.append(subscription)
        save_subscribers(subs)

    return {"status": "subscribed", "total": len(subs)}


# ============================================================
# PUSH KÜLDÉSE MINDEN FELIRATKOZOTTNAK
# ============================================================
def send_push_to_all(data: dict):
    """
    Bármilyen adathoz használható:
    - Live tipp
    - Chat üzenet
    - Figyelmeztetés
    - Kombi kész
    """

    subs = load_subscribers()
    dead_subs = []

    for sub in subs:
        try:
            webpush(
                subscription_info=sub,
                data=json.dumps(data),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims={"sub": VAPID_EMAIL},
            )
        except WebPushException:
            dead_subs.append(sub)

    # halott feliratkozók törlése
    if dead_subs:
        subs = [s for s in subs if s not in dead_subs]
        save_subscribers(subs)

    return {"sent": len(subs), "removed": len(dead_subs)}
