# ============================================================
# Data Normalizer – egységes bemeneti adatformáló réteg
# ============================================================

class DataNormalizer:
    """
    A rendszer összes engine-jének egységes és tiszta bemeneti formát
    biztosít. Bármilyen nyers adatból szabványosított dictionary-t készít.
    """

    @staticmethod
    def normalize(raw_input: dict):
        """
        Minden motor számára közös bemeneti formát készít.
        Ha egy kulcs hiányzik, létrehozzuk üres értékkel.
        """

        normalized = {
            "match_data": raw_input.get("match_data", {}),
            "stats": raw_input.get("stats", {}),
            "sequence": raw_input.get("sequence", []),
            "graph": raw_input.get("graph", None),
            "player_stats": raw_input.get("player_stats", {}),
            "live_feed": raw_input.get("live_feed", {}),
            "metadata": raw_input.get("metadata", {}),
        }

        # Extra: ha odds kulcsok szétszórtak → egybe gyűjtjük
        if "odds" in raw_input:
            normalized["match_data"]["odds"] = raw_input["odds"]

        return normalized
