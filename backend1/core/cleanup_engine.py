# ============================================================
# Cleanup Engine – rendezés több ezer tipphez
# ============================================================

class CleanupEngine:
    """
    Több ezer eseményt tisztít:
    - duplikált event_id törlése
    - 0 value törlése
    - low liquidity törlése
    - hibás odds törlése
    """

    def clean(self, events):
        cleaned = []
        seen = set()

        for e in events:
            if e["id"] in seen:
                continue
            seen.add(e["id"])

            if not e.get("liquid", False):
                continue

            if e.get("odds", 0) <= 1.01:
                continue

            if e.get("value", 0) <= 1.00:
                continue

            cleaned.append(e)

        return cleaned
