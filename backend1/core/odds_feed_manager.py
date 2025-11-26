# ============================================================
# ODDS FEED MANAGER – Full System Version
# ------------------------------------------------------------
# Feladata:
# - API kliensek meghívása (Betfair, Pinnacle, OddsAPI)
# - Adapterekkel normalizálás
# - Merge Engine-nel egységesítés
# - StrategyEngine-hez készített lista visszaadása
# ============================================================

import asyncio

from feeds.odds_api_client import OddsAPIClient
from feeds.betfair_adapter import BetfairAdapter
from feeds.pinnacle_adapter import PinnacleAdapter
from feeds.odds_merge_engine import OddsMergeEngine


class OddsFeedManager:
    """
    Egyetlen modul, amely lehívja *minden* odds forrás adatait,
    normalizálja és egyesíti őket a StrategyEngine számára.
    """

    def __init__(self):
        self.client = OddsAPIClient()
        self.betfair = BetfairAdapter()
        self.pinnacle = PinnacleAdapter()
        self.merge = OddsMergeEngine()

    # ------------------------------------------------------------
    # ODDSOK BETÖLTÉSE PARALLEL (3x gyorsabb)
    # ------------------------------------------------------------
    async def load_all_odds(self, sport="soccer"):
        """
        Betölti az összes odds forrást:
        - Betfair
        - Pinnacle
        - OddsAPI
        """

        # 1) Raw odds fetch (nyers adatok)
        raw_feeds = await self.client.fetch_all_sources(sport)

        # 2) Normalizálás source-onként
        normalized_betfair = self.betfair.normalize_list(raw_feeds.get("betfair", []))
        normalized_pinnacle = self.pinnacle.normalize_list(raw_feeds.get("pinnacle", []))
        normalized_oddsapi = raw_feeds.get("oddsapi", [])

        # Minden forrást normalizált struktúrával kell adni
        normalized_feeds = {
            "betfair": normalized_betfair,
            "pinnacle": normalized_pinnacle,
            "oddsapi": normalized_oddsapi
        }

        # 3) Merge (összefűzés, value rendezés, duplikáció törlés)
        merged = self.merge.merge_all(normalized_feeds)

        return merged

    # ------------------------------------------------------------
    # SYNCHRONOUS WRAPPER (FastAPI kompatibilitás miatt)
    # ------------------------------------------------------------
    def load(self, sport="soccer"):
        """
        Synchronous wrapper – FastAPI endpointból hívható.
        """
        return asyncio.run(self.load_all_odds(sport))
