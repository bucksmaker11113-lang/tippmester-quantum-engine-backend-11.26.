# ============================================================
# OrchestratorMain – a rendszer központi vezérlő rétege
# ============================================================

from backend.core.engine_registry import EngineRegistry


class OrchestratorMain:
    """
    A végső, egységes orchestrator.
    Ez futtatja a rendszert:
    - betölti az engine-eket
    - futtatja őket egységes pipeline-on
    - összegyűjti az eredményeket
    """

    def __init__(self, config: dict):
        self.config = config
        self.engines_to_run = config.get("engines", [])

    # ---------------------------------------------------------
    # ENGINES BETÖLTÉSE
    # ---------------------------------------------------------
    def load_engines(self):
        loaded = []
        for engine_name in self.engines_to_run:
            instance = EngineRegistry.create_instance(engine_name)
            loaded.append(instance)
        return loaded

    # ---------------------------------------------------------
    # PIPELINE FUTTATÁSA
    # ---------------------------------------------------------
    def run_pipeline(self, input_data):
        engines = self.load_engines()
        results = []

        for engine in engines:
            try:
                print(f"[ORCHESTRATOR] Futtatás: {engine.name}")
                output = engine.run_pipeline(input_data)
                results.append(output)
            except Exception as e:
                print(f"[HIBA] Engine hiba: {engine.name} → {e}")

        return {
            "total_engines": len(engines),
            "results": results
        }

    # ---------------------------------------------------------
    # TELJES FUTÁS
    # ---------------------------------------------------------
    def execute(self, input_data):
        """
        A fő belépési pont.
        """
        print("[ORCHESTRATOR] Rendszer indul...")
        return self.run_pipeline(input_data)
