# ============================================================
# TippmixPro Crosscheck Engine
# ============================================================

class TippmixProCrosscheck:
    """
    Megnézi, hogy egy esemény elérhető-e a TippmixPron.
    Ha igen → újraszámolja a value-t Tippmix odds alapján.
    Ha nem → a tipp törlendő.
    """

    def __init__(self, tippmix_api=None):
        self.api = tippmix_api or self.mock_api

    # Mock API – valódi Tippmix scraper helyére később csatlakozik
    def mock_api(self, event_id):
        return {
            "available": True,
            "odds": {
                "market": "over/under",
                "over": 1.78,
                "under": 1.92
            }
        }

    # ---------------------------------------------------------
    def check_event(self, event):
        response = self.api(event["id"])

        if not response["available"]:
            return None

        # új value számítás Tippmix odds alapján
        tippmix_odds = max(response["odds"].values())
        fair = event.get("fair_odds", event["odds"])
        new_value = tippmix_odds / fair

        event["tippmix_available"] = True
        event["tippmix_odds"] = tippmix_odds
        event["value"] = new_value

        return event
