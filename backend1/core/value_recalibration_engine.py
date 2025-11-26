# ============================================================
# Value Recalibration Engine
# ============================================================

class ValueRecalibrator:
    """
    Mivel a Poisson, MonteCarlo, GNN, LSTM más value-skálát ad,
    itt egységesítjük őket egy központi normál skálára.
    """

    def rescale(self, event):
        v = event.get("value", 1.0)

        # Normál skála 1.00 – 1.20 között
        if v < 1.00:
            v = 1.00
        if v > 1.50:
            v = 1.50

        # Egységesítve
        event["value"] = 1.00 + (v - 1.00) * 0.6
        return event
