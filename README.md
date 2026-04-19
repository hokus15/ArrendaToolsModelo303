# ArrendaTools Modelo 303
![License](https://img.shields.io/github/license/hokus15/ArrendaToolsModelo303)
[![Build Status](https://github.com/hokus15/ArrendaToolsModelo303/actions/workflows/main.yml/badge.svg)](https://github.com/hokus15/ArrendaToolsModelo303/actions)
![GitHub last commit](https://img.shields.io/github/last-commit/hokus15/ArrendaToolsModelo303?logo=github)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/hokus15/ArrendaToolsModelo303?logo=github)

Módulo de Python que genera un string para la importación de datos en el modelo 303 de la Agencia Tributaria de España para los ejercicios soportados 2025 y 2026 (PRE 303 - Servicio ayuda modelo 303). El string generado se puede guardar en un fichero para importarlo en el modelo 303 para la presentación trimestral del IVA.

## Limitaciones

Este módulo está diseñado específicamente para facilitar la presentación del IVA trimestral de arrendadores de locales y viviendas urbanas que no realicen ninguna otra actividad. **No es válido para otros casos**, por lo que se recomienda su uso exclusivamente en el contexto mencionado.

Es importante tener en cuenta que este módulo no es aplicable en los siguientes casos:

- Si durante el trimestre se han realizado:
  - Ventas de inmuebles
  - Arrendamientos con opción de compra
  - Servicios complementarios de hostelería
  - Adquisiciones de bienes o servicios a proveedores extranjeros o establecidos en Canarias, Ceuta o Melilla (a excepción de obras realizadas por extranjeros).
- En declaraciones mensuales.
- En el régimen simplificado.
- En el Régimen Especial del Criterio de Caja.
- Si el % atribuible a la Administración del Estado es distinto de 100%.
- En el IVA a la importación liquidado por la Aduana pendiente de ingreso.
- En autoliquidaciones complementarias (opción y número de justificante).
- En casos en los que el volumen de operaciones anual sea igual a 0.
- Cuando existan cuotas pendientes de compensar de periodos anteriores.
- En la cuenta corriente tributaria - ingreso.
- En la cuenta corriente tributaria - devolución.
- En la devolución por transferencia al extranjero.

Por lo tanto, se recomienda al usuario verificar que se cumplen todas las condiciones necesarias antes de utilizar este módulo para la presentación del IVA trimestral.

## Descargo de responsabilidad

Este proyecto es una herramienta técnica para ayudar a generar un fichero importable en el modelo 303. **No constituye asesoramiento fiscal, contable ni jurídico**.

Este proyecto **no está afiliado, patrocinado, aprobado ni validado por la Agencia Estatal de Administración Tributaria (AEAT)**. Corresponde exclusivamente al usuario comprobar la normativa aplicable, los diseños de registro vigentes y el resultado final antes de presentar cualquier autoliquidación.

El software se distribuye bajo licencia MIT y se proporciona **"tal cual" ("AS IS")**, sin garantías de ningún tipo, expresas o implícitas, incluyendo (sin limitación) exactitud, idoneidad para un propósito concreto, ausencia de errores, continuidad de funcionamiento o adecuación a cambios normativos.

En la máxima medida permitida por la legislación aplicable, el autor y colaboradores no asumen responsabilidad por daños, pérdidas, sanciones, recargos, intereses, costes o reclamaciones derivados del uso, mal uso o imposibilidad de uso de la librería, incluidos errores en datos de entrada, configuraciones incorrectas, cambios de criterio de la AEAT o falta de actualización del software.

El usuario es el único responsable de:

- La veracidad, integridad y actualización de los datos introducidos.
- La revisión manual del fichero generado antes de su presentación.
- La validación final ante la AEAT y el cumplimiento de sus obligaciones fiscales.

Este descargo se interpreta **sin perjuicio de los límites imperativos de responsabilidad que no puedan excluirse por ley**.

## Requisitos

Este módulo requiere Python 3.10 o superior.

## Uso

El primer paso es recopilar la información necesaria para el trimestre fiscal que desees realizar la declaración. Esta información incluye datos del contribuyente, datos financieros y otros detalles específicos del trimestre. Algunos campos son obligatorios, como el periodo, la base imponible y el NIF del contribuyente, mientras que otros son opcionales dependiendo del contexto, como el volumen anual de operaciones (obligatorio solo en el cuarto trimestre).

Usando la clase `Modelo303Data` proporcionada por el módulo, puedes definir los datos requeridos. Cada campo tiene validaciones, como la longitud máxima, el formato y la obligatoriedad.

El módulo incluye una función `get_generator(fiscal_year)` para obtener el generador del ejercicio deseado y un método `generate(data)` que devuelve el string listo para importar.

Ejemplo completo:

```python
from decimal import Decimal
from pathlib import Path

from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.application.facade import get_generator
from arrendatools.modelo303.domain.enums import Period

datos = Modelo303Data(
    periodo=Period.FOURTH_QUARTER,
    version="1.00",
    nif_empresa_desarrollo="12345678X",
    razon_social="DE LOS PALOTES PERICO",
    nif_contribuyente="12345678X",
    iban="ES0012341234123412341234",
    base_imponible=Decimal("10000.00"),
    base_gastos_bienes_y_servicios=Decimal("500.00"),
    cuota_gastos_bienes_y_servicios=Decimal("105.00"),
    base_adquisiones_bienes_inversion=Decimal("3000.00"),
    cuota_adquisiones_bienes_inversion=Decimal("630.00"),
    volumen_anual_operaciones=Decimal("20000.00"),
)

generador = get_generator(2025)
contenido = generador.generate(datos)

# Guardar en fichero para importar en el modelo 303
Path("modelo303.303").write_text(contenido)
```

## Arquitectura

El proyecto sigue una arquitectura por capas con un **motor de renderizado basado en schemas YAML**:

```
application/
  facade.py          → API pública: get_generator(fiscal_year) → Modelo303Generator
  generator.py       → Modelo303Generator(fiscal_year, schema).generate(data) → str
  data.py            → Modelo303Data (entrada validada con Pydantic)

domain/
  model.py           → Modelo303Model (cálculos de casillas)
  enums.py           → Period

infrastructure/
  schema.py          → Tipos internos: SchemaSpec, PageSpec, FieldSpec, Source, FieldType
  schema_loader.py   → load_schema(path | Traversable) → SchemaSpec
  schema_validator.py → validate_schema(schema)
  schema_renderer.py → render_schema(schema, model) → str
  schema_registry.py → SUPPORTED_SCHEMAS, get_schema(fiscal_year)
  builtins.py        → BUILTIN_REGISTRY: funciones Python invocables desde el schema
  formatting.py      → Utilidades de formateo de campos numéricos y con signo
  schemas/
    2025.1.yaml      → Schema completo del ejercicio 2025
    2026.1.yaml      → Schema completo del ejercicio 2026

tools/
  generate_schema.py → Genera un schema YAML a partir del Excel oficial de la AEAT
```

### Flujo de datos

```
Modelo303Data
     │
     ▼
Modelo303Model.from_data()   ← calcula casillas derivadas
     │
     ▼
render_schema(schema, model) ← itera páginas y campos del schema YAML
     │  ├─ source=constant  → valor literal del schema
     │  ├─ source=default   → valor por defecto del schema
     │  ├─ source=model     → atributo del modelo (casilla_XX)
     │  ├─ source=builtin   → función registrada en BUILTIN_REGISTRY
     │  └─ source=formula   → expresión aritmética evaluada de forma segura (sin eval)
     │
     ▼
String de importación (formato AEAT)
```

### Sources de un campo en el schema

| `source`    | Descripción                                                                          | Clave YAML requerida |
|-------------|--------------------------------------------------------------------------------------|----------------------|
| `constant`  | Valor literal fijo (e.g. identificadores de página, tipo de declaración fijo)        | `value`              |
| `default`   | Valor por defecto (puede ser sobreescrito si se añade lógica futura)                 | `value`              |
| `model`     | Se lee del atributo `name` del campo en `Modelo303Model`                              | —                    |
| `builtin`   | Llama a una función registrada en `BUILTIN_REGISTRY`                                 | `function`           |
| `formula`   | Expresión aritmética sobre atributos del modelo (`casilla_X op casilla_Y`)           | `expr`               |

### Páginas condicionales

Una página puede tener `include_when: fourth_quarter` para que solo se incluya en el cuarto trimestre. El valor por defecto es `always`.

---

## Cómo añadir un nuevo ejercicio

Para añadir soporte para un año nuevo (por ejemplo, `2027`):

### 1. Generar el schema YAML inicial desde el Excel de la AEAT

```bash
python tools/generate_schema.py "specs/2027/YYYYMMDD - DR303e27v101.xlsx" \
    --year 2027 --revision 1.01 \
    --output src/arrendatools/modelo303/infrastructure/schemas/2027.1.yaml
```

La herramienta genera un schema con campos `source=constant` para las constantes detectadas y `source=model` para el resto. Las advertencias (`!`) indican los campos que requieren revisión manual.

### 2. Revisar y completar el schema YAML

Abre `schemas/2027.1.yaml` y ajusta:

- Los campos con `source=model` se resuelven usando el campo `name` del campo en el schema. El nombre debe coincidir exactamente con el atributo correspondiente en `Modelo303Model` (p.ej. `casilla_XX`).
- Si un campo es el resultado de un cálculo entre casillas, usa `source: formula` con `expr: casilla_A - casilla_B + casilla_C`. Solo se permiten operaciones aritméticas básicas (`+`, `-`, `*`, `/`) sobre atributos numéricos del modelo.
- Si un campo requiere lógica de negocio compleja (tipo de declaración, marca SEPA, etc.), usa `source: builtin` con `function: nombre_funcion`. La función debe estar registrada en `BUILTIN_REGISTRY`.
- Si el cuarto trimestre tiene páginas adicionales (e.g. sección `DID`, volumen anual), añade `include_when: fourth_quarter` a esa página.

### 3. Registrar el schema en el registry

Edita `src/arrendatools/modelo303/infrastructure/schema_registry.py` y añade la entrada:

```python
SUPPORTED_SCHEMAS: dict[int, str] = {
    2025: "2025.1.yaml",
    2026: "2026.1.yaml",
    2027: "2027.1.yaml",   # ← nuevo
}
```

Esto es el único cambio de código necesario si el nuevo ejercicio no introduce casillas nuevas ni lógica de negocio adicional.

### 4. Revisar el schema YAML si hay campos numéricos nuevos

El renderer escala automáticamente los valores `Decimal` a céntimos (`×100`) para todos los campos con `field_type: numeric` o `field_type: numeric_signed`. Los valores que el modelo retorna como `str` (año, periodo, flags de un carácter) se pasan tal cual sin conversión, ya que la rama `isinstance(raw_value, str)` los atrapa antes.

No hay configuración adicional necesaria: el tipo Python del valor y el `field_type` del schema son suficientes para determinar el formateo.

### 5. Revisar `model.py` si hay nuevas casillas de datos

Si el nuevo ejercicio tiene casillas de entrada de datos nuevas que no existen en `Modelo303Model` (`src/arrendatools/modelo303/domain/model.py`):

- Añade el atributo como slot de `Modelo303Model` con tipo `Decimal` y valor por defecto apropiado.
- Si es una casilla derivada de otras (calculada), añade la lógica de cálculo directamente en `from_data()`.
- Mantén siempre operaciones monetarias con `Decimal` y `quantize(Decimal("0.01"), ...)`.

### 6. Registrar funciones builtin nuevas si las hay

Si el nuevo ejercicio introduce un campo con lógica que no puede expresarse como fórmula, añade la función en `src/arrendatools/modelo303/infrastructure/builtins.py`:

```python
BUILTIN_REGISTRY: dict[str, Callable] = {
    ...,
    "mi_funcion_2027": lambda model: ...,
}
```

### 7. Añadir tests del nuevo ejercicio

- Crea `tests/test_generator_tax_year_2027.py` tomando como base `test_generator_tax_year_2026.py`.
- Añade ficheros golden en `tests/golden/2027/` para los escenarios 1T/2T/3T, 4T positivo, 4T negativo y sin IBAN.
- Actualiza `tests/test_modelo303_factory.py` para incluir 2027 en los años soportados.
- Ejecuta `pytest tests/ -v` para validar que todos los tests pasan.

### Checklist mínimo

- [ ] `get_generator(2027)` devuelve un generador sin error.
- [ ] `test_all_schema_fields_exist_in_catalog` pasa (todos los campos del schema están en el catálogo).
- [ ] `test_model_and_catalog_can_render_every_catalog_field` pasa.
- [ ] Golden tests de 2027 pasan (1T/2T/3T, 4T y sin IBAN).
- [ ] `pytest tests/ -v` sin fallos.

Ahora ya puedes generar el fichero utilizando el método correspondiente. Este método convierte los datos proporcionados en un formato compatible con el sistema de la Agencia Tributaria.
Por ejemplo:


```python
datos_fichero = modelo.generate(datos)
```

A continuación se muestra un ejemplo completo de cómo crear un objeto GeneradorModelo303 para el ejercicio 2025 y generar un archivo con los datos del modelo:

```python
from arrendatools.modelo303.application.facade import get_generator
from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period

period = Period.THIRD_QUARTER
anyo_fiscal = 2025
nif_empresa_desarrollo = "12345678X"
version = "v1.0"
nif_contribuyente = "12345678X"
razon_social = "DE LOS PALOTES PERICO"
iban = "ES0012341234123412341234"
base_imponible = 2000.00
base_gastos_bienes_y_servicios = 2500.0
cuota_gastos_bienes_y_servicios = 525.0
base_adquisiones_bienes_inversion = 0.0
cuota_adquisiones_bienes_inversion = 0.0
volumen_anual_operaciones = None

datos_modelo = Modelo303Data(
    ejercicio=period,
    nif_empresa_desarrollo=nif_empresa_desarrollo,
    version=version,
    razon_social=razon_social,
    nif_contribuyente=nif_contribuyente,
    iban=iban,
    base_imponible=base_imponible,
    base_gastos_bienes_y_servicios=base_gastos_bienes_y_servicios,
    cuota_gastos_bienes_y_servicios=cuota_gastos_bienes_y_servicios,
    base_adquisiones_bienes_inversion=base_adquisiones_bienes_inversion,
    cuota_adquisiones_bienes_inversion=cuota_adquisiones_bienes_inversion,
    volumen_anual_operaciones=volumen_anual_operaciones,
)

modelo = get_generator(anyo_fiscal)

datos_fichero = modelo.generate(datos_modelo)
print(datos_fichero)

with open(f"{nif_contribuyente}_{anyo_fiscal}_{period.value}.303", "w") as archivo:
    archivo.write(datos_fichero)
```

Es importante tener en cuenta que, aunque el ejemplo anterior es funcional, es posible que la importación en la web de la Agencia Tributaria falle en las validaciones adicionales que esta realiza, por lo que se deben proporcionar los datos correctos para poder importar correctamente el modelo en la web de la Agencia Tributaria. 
