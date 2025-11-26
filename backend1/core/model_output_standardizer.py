# ============================================================
# Model Output Standardizer – egységes eredményformátum
# ============================================================

class ModelOutputStandardizer:
    """
    A különböző motorok outputjait tiszta, szabványos formára alakítja.
    Ezzel minden engine összehangoltan tud működni az orchestrator alatt.
    """

    @staticmethod
    def standardize(raw_output: dict, engine_name: str):
        """
        Az output minimális elvárásai:
        {
            "engine": str,
            "probabilities": {} vagy [],
            "confidence": float,
            "raw_output": {}
        }
        """

        if raw_output is None:
            raw_output = {}

        # Probabilities kulcs biztosítása
        probabilities = (
            raw_output.get("probabilities")
            if isinstance(raw_output, dict)
            else None
        )

        # Confidence érték normalizálása
        confidence = (
            raw_output.get("confidence", 0.5)
            if isinstance(raw_output, dict)
            else 0.5
        )

        standardized = {
            "engine": engine_name,
            "probabilities": probabilities,
            "confidence": confidence,
            "raw_output": raw_output
        }

        return standardized
