# ============================================================
# Engine Registry – dinamikus engine-nyilvántartó
# ============================================================

from typing import Dict, Type
from backend.core.engine_base import EngineBase


class EngineRegistry:
    """
    Egyetlen központi regiszter minden engine számára.
    Az orchestrator ezt használja betöltésre.
    """

    _registry: Dict[str, Type[EngineBase]] = {}

    @classmethod
    def register(cls, engine_class):
        """
        Dekorátor az engine-ek egyszerű regisztrálásához.
        Használat:
        
        @EngineRegistry.register
        class PoissonEngine(EngineBase):
            ...
        """
        name = engine_class.__name__.lower()
        cls._registry[name] = engine_class
        print(f"[REGISTRY] Engine regisztrálva: {name}")
        return engine_class

    @classmethod
    def get_engine(cls, name: str):
        """
        Engine példány lekérése név alapján.
        """
        key = name.lower()
        if key not in cls._registry:
            raise ValueError(f"EngineRegistry: '{name}' engine ismeretlen!")
        return cls._registry[key]

    @classmethod
    def list_engines(cls):
        """
        Az összes elérhető engine kiíratása.
        """
        return list(cls._registry.keys())

    @classmethod
    def create_instance(cls, name: str, config: dict = None):
        """
        Példányosít egy engine-t a nevéből.
        """
        engine_class = cls.get_engine(name)
        return engine_class(name=name, config=config)
