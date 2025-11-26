# ============================================================
# Daily Scheduler
# ============================================================

import datetime
import time


class DailyScheduler:
    """
    Egyszerű időzítő motor:
    - Reggel 9:00 → single tippek
    - Délután 12:00 → kombi
    - 14:00 után → live tippek monitor
    """

    def __init__(self, strategy_engine, fetcher):
        self.strategy = strategy_engine
        self.fetcher = fetcher

    def run(self):
        while True:
            now = datetime.datetime.now()

            if now.hour == 9 and now.minute == 0:
                data = self.fetcher.get_all_events()
                print("→ Single tippek generálása...")
                print(self.strategy.generate_daily_picks(data, []))

            if now.hour == 12 and now.minute == 0:
                data = self.fetcher.get_all_events()
                print("→ Kombi generálása...")
                print(self.strategy.generate_daily_picks(data, []))

            if now.hour >= 14:
                live = self.fetcher.get_live_events()
                print("→ Live figyelés...")
                print(self.strategy.generate_daily_picks([], live))

            time.sleep(60)
