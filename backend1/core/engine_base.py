# ============================================================
# EngineBase – egységes alaposztály minden predikciós motorhoz
# ============================================================

class EngineBase:
    """
    Minden engine egységes alapstruktúrája.
    Csak ezt kell örökölni és három metódust implementálni:
    - prepare()    → input normalizálása
    - run_model()  → modell futtatás
    - postprocess() → output standardizálása
    """

    def __init__(self, name: str, config: dict = None):
        self.name = name
        self.config = config if config else {}

    # ------------------------------
    # 1) INPUT NORMALIZÁLÁS
    # ------------------------------
    def prepare(self, raw_input):
        """
        A motorok bemenetét egységes formára hozza.
        Ezt minden engine saját magára szabja.
        """
        return raw_input

    # ------------------------------
    # 2) MODELL FUTTATÁS
    # ------------------------------
    def run_model(self, prepared_input):
        """
        Ez maga a modell futása.
        Return → engine-specifikus formátum.
        """
        raise NotImplementedError(
            f"{self.name}: run_model() nincs implementálva!"
        )

    # ------------------------------
    # 3) OUTPUT STANDARDIZÁLÁS
    # ------------------------------
    def postprocess(self, model_output):
        """
        A különböző engine-ek változatos outputját egységesítjük.
        Return példa:
        {
            'engine': 'poisson',
            'probabilities': {...},
            'confidence': 0.82,
            'raw_output': {...}
        }
        """
        return {
            "engine": self.name,
            "raw_output": model_output,
            "confidence": 1.0
        }

    # ------------------------------
    # 4) TELJES PIPELINE FUTTATÁSA
    # ------------------------------
    def run_pipeline(self, raw_input):
        """
        A teljes folyamatot egységesen futtatja:
        prepare() → run_model() → postprocess()
        Ezt hívja a master orchestrator.
        """
        prepared = self.prepare(raw_input)
        model_output = self.run_model(prepared)
        standardized = self.postprocess(model_output)
        return standardized
