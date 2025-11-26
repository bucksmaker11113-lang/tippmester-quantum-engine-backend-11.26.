# ============================================================
# Bankroll History Logger
# ============================================================

import json
import datetime


class BankrollLogger:
    """
    Minden tipp után elmenti:
    - bankroll változás
    - tét
    - value
    - eredmény (win/loss)
    - sportág
    """

    def __init__(self, path="bankroll_history.json"):
        self.path = path

    def log(self, category, before, after, stake, event):
        record = {
            "time": str(datetime.datetime.now()),
            "category": category,
            "bankroll_before": before,
            "bankroll_after": after,
            "stake": stake,
            "event_id": event["id"],
            "sport": event.get("sport"),
            "value": event.get("value"),
            "confidence": event.get("confidence"),
        }

        history = []
        try:
            with open(self.path, "r") as f:
                history = json.load(f)
        except:
            pass

        history.append(record)

        with open(self.path, "w") as f:
            json.dump(history, f, indent=2)
