import importlib
from pathlib import Path

from arrendatools.modelo303.generador import Modelo303Generador


class Modelo303Factory:
    GENERADORES_PATH = Path(__file__).parent / "generadores"
    GENERADOR_PREFIX = "generador_ejercicio_"

    @staticmethod
    def obtener_generador_modelo303(ejercicio: int) -> Modelo303Generador:
        """Obtiene el generador del modelo 303 para el ejercicio especificado."""
        # Nombre del módulo en términos de Python (relativo al paquete principal)
        nombre_modulo = f"arrendatools.modelo303.generadores.{Modelo303Factory.GENERADOR_PREFIX}{ejercicio}"
        # Ruta física al archivo del módulo
        ruta_modulo = (
            Modelo303Factory.GENERADORES_PATH
            / f"{Modelo303Factory.GENERADOR_PREFIX}{ejercicio}.py"
        )

        if not ruta_modulo.exists():
            raise ValueError(
                f"No existe un generador para el ejercicio {ejercicio}"
            )

        try:
            # Importa dinámicamente el módulo del generador
            modulo = importlib.import_module(nombre_modulo)
            # Busca una clase que implemente Modelo303Generador
            for atributo in dir(modulo):
                atributo_clase = getattr(modulo, atributo)
                if (
                    isinstance(atributo_clase, type)
                    and issubclass(atributo_clase, Modelo303Generador)
                    and atributo_clase is not Modelo303Generador
                ):
                    return atributo_clase(ejercicio)
        except Exception as e:
            raise ImportError(
                f"Error al cargar el generador para el ejercicio {ejercicio}: {e}"
            )

        raise ValueError(
            f"No se encontró una clase válida en el módulo para el ejercicio {ejercicio}"
        )
