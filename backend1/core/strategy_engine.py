# ============================================================
# STRATEGY ENGINE – FULL SYSTEM VERSION
# ============================================================
# Funkciók:
# - 4 single tipp (foci, kosar, hoki, tenisz)
# - Kombi szelvény (4–5 esemény)
# - Live tippek (14:00 után)
# - Kelly stake számítás (1–2%)
# - Külön bankroll poolok
# - Odds feed + value skálázás kompatibilis
# ============================================================

import datetime


class StrategyEngine:
    """
    Teljes tippstratégiai motor:
    - Value + confidence alapú rendezés
    - Sportág súlyozás
    - Kelly stake számítás
    - Napi single / kombi / live tippek generálása
    """

    def __init__(self, initial_single, initial_kombi, initial_live):
        self.single_bankroll = initial_single
        self.kombi_bankroll = initial_kombi
        self.live_bankroll = initial_live

        # Sportág súlyok (single tippek)
        self.sport_weights = {
            "foci": 0.60,
            "kosar": 0.20,
            "hoki": 0.10,
            "tenisz": 0.10
        }

    # ============================================================
    # SINGLE TIPP KIVÁLASZTÁS
    # ============================================================
    def select_single_tips(self, all_events):
        """
        Single tippek kiválasztása sportáganként egy darab,
        value + confidence + súly kombináció alapján.
        """

        selected = {}

        for sport in ["foci", "kosar", "hoki", "tenisz"]:

            sport_events = [
                e for e in all_events
                if e.get("sport") == sport
                and e.get("liquid", False)
                and e.get("value", 1.0) > 1.0
                and e.get("confidence", 0) > 0.60
            ]

            if not sport_events:
                continue

            # pontszámítás: (value * confidence * sport_weight)
            for e in sport_events:
                e["score"] = (
                    e["value"] *
                    e["confidence"] *
                    self.sport_weights[sport]
                )

            # legjobb választása
            best = sorted(sport_events, key=lambda x: x["score"], reverse=True)[0]
            selected[sport] = best

        return selected

    # ============================================================
    # KELLY ALAPÚ TÉT → 1–2%
    # ============================================================
    def calculate_single_stake(self, event, kelly_factor=1.0):
        kelly_raw = event.get("kelly", 0.02)   # value engine adja
        base_percent = min(0.02, max(0.01, kelly_raw * kelly_factor))

        stake = self.single_bankroll * base_percent
        return round(stake, 2)

    # ============================================================
    # KOMBI SZELVÉNY (4–5 esemény)
    # ============================================================
    def select_kombi(self, all_events, single_events):

        # single meccsek ID-jének kizárása
        single_ids = {ev["id"] for ev in single_events.values()}

        candidates = [
            e for e in all_events
            if e.get("liquid")
            and e.get("value", 1.0) > 1.02
            and e.get("confidence", 0) > 0.58
            and e["id"] not in single_ids
        ]

        candidates = sorted(
            candidates,
            key=lambda x: x["value"] * x["confidence"],
            reverse=True
        )

        return candidates[:5]  # 4–5 esemény

    def kombi_stake(self):
        stake = self.kombi_bankroll * 0.02
        return round(stake, 2)

    # ============================================================
    # LIVE TIPPEK (14:00 után)
    # ============================================================
    def select_live_tips(self, live_events, max_tips=2):

        now = datetime.datetime.now()
        if now.hour < 14:
            return []

        candidates = [
            e for e in live_events
            if e.get("odds_spike", False)
            and e.get("value", 1.0) > 1.03
            and e.get("confidence", 0) > 0.62
        ]

        candidates = sorted(
            candidates,
            key=lambda x: x["value"] * x["confidence"],
            reverse=True
        )

        return candidates[:max_tips]

    def live_stake(self):
        stake = self.live_bankroll * 0.01
        return round(stake, 2)

    # ============================================================
    # FŐ KIVÁLASZTÁSI FOLYAMAT – NAPI TIPPEK
    # ============================================================
    def generate_daily_picks(self, all_events, live_events):

        # Single
        single = self.select_single_tips(all_events)
        single_stakes = {
            sport: self.calculate_single_stake(ev)
            for sport, ev in single.items()
        }

        # Kombi
        kombi = self.select_kombi(all_events, single)
        kombi_stake = self.kombi_stake()

        # Live
        live = self.select_live_tips(live_events)
        live_stakes = [self.live_stake() for _ in live]

        return {
            "single": single,
            "single_stakes": single_stakes,
            "kombi": kombi,
            "kombi_stake": kombi_stake,
            "live": live,
            "live_stakes": live_stakes
        }
