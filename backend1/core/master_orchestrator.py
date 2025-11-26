# ============================================================
# MASTER ORCHESTRATOR (ÚJ VERZIÓ)
# A rendszer központi vezérlő rétege – egységes, stabil, tiszta
# ============================================================

from backend.core.engine_registry import EngineRegistry
from backend.core.data_normalizer import DataNormalizer
from backend.core.model_output_standardizer import ModelOutputStandardizer


class MasterOrchestrator:
    """
    A teljes rendszer fő vezérlője.
    - normalizálja az inputot
    - betölti az engine-eket
    - futtatja a pipeline-t
    - standardizálja a kimeneteket
    """

    def __init__(self, config: dict):
        self.config = config

        # A config-ben felsorolt engine-neveket futtatjuk
        self.engines_to_run = config.get("engines", [])
        if not self.engines_to_run:
            print("[FIGYELEM] Nincsenek engine-ek megadva a config-ben.")

    # ---------------------------------------------------------
    # INPUT NORMALIZÁLÁSA
    # ---------------------------------------------------------
    def normalize_input(self, raw_input):
        return DataNormalizer.normalize(raw_input)

    # ---------------------------------------------------------
    # ENGINE-EK BETÖLTÉSE
    # ---------------------------------------------------------
    def load_engines(self):
        loaded = []

        for engine_name in self.engines_to_run:
            try:
                instance = EngineRegistry.create_instance(engine_name)
                loaded.append(instance)
                print(f"[ORCHESTRATOR] Betöltve: {engine_name}")
            except Exception as e:
                print(f"[HIBA] Engine betöltési hiba: {engine_name} → {e}")

        return loaded

    # ---------------------------------------------------------
    # PIPELINE FUTTATÁSA ENGINE-ENKÉNT
    # ---------------------------------------------------------
    def run_pipeline(self, normalized_input):
        engines = self.load_engines()
        results = []

        for engine in engines:
            try:
                print(f"[ORCHESTRATOR] Futtatás: {engine.name}")
                raw_output = engine.run_pipeline(normalized_input)

                standardized_output = ModelOutputStandardizer.standardize(
                    raw_output, engine.name
                )

                results.append(standardized_output)

            except Exception as e:
                print(f"[HIBA] Pipeline futtatási hiba: {engine.name} → {e}")

        return results

    # ---------------------------------------------------------
    # FŐ INDÍTÁSI METÓDUS
    # ---------------------------------------------------------
    def execute(self, raw_input):
        print("[ORCHESTRATOR] Rendszer indul...")

        # 1) normalizáljuk az inputot
        normalized = self.normalize_input(raw_input)

        # 2) futtatjuk az engine-ek pipeline-jait
        results = self.run_pipeline(normalized)

        print("[ORCHESTRATOR] Kész.")

        return {
            "input": normalized,
            "results": results,
            "engine_count": len(results)
        }
