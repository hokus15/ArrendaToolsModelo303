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

Usando la clase Modelo303Data proporcionada por el módulo, puedes definir los datos requeridos. Cada campo tiene validaciones, como la longitud máxima, el formato y la obligatoriedad.
Por ejemplo:

```python
from arrendatools.modelo303.application.data import Modelo303Data
from arrendatools.modelo303.domain.enums import Period

datos = Modelo303Data(
    ejercicio=Period.FOURTH_QUARTER,
    version="1.0",
    nif_empresa_desarrollo="12345678X",
    razon_social="DE LOS PALOTES PERICO",
    nif_contribuyente="12345678X",
    iban="ES0012341234123412341234",
    base_imponible=10000.00,
    base_gastos_bienes_y_servicios=500.00,
    cuota_gastos_bienes_y_servicios=105.00,
    base_adquisiones_bienes_inversion=3000.00,
    cuota_adquisiones_bienes_inversion=630.00,
    volumen_anual_operaciones=20000.00
)
```

El módulo incluye una API funcional para obtener el generador según ejercicio.
Por ejemplo:

```python
from arrendatools.modelo303.application.facade import get_generator

modelo = get_generator(2025)
```

## Arquitectura de generación por ejercicio

El proyecto utiliza un **único generador** para todos los ejercicios soportados:

- Generador único: `arrendatools.modelo303.application.generator.Modelo303Generator`
- Layouts por año: `arrendatools.modelo303.infrastructure.layout_registry.LAYOUTS`

Cada ejercicio define su layout completo: registro de apertura, secciones `00`, `01`, `02`, `03`, `04`, `05`, `DID` y registro de cierre.

### Cómo añadir un nuevo ejercicio

Para añadir un nuevo año (por ejemplo, `2027`) hay que revisar **4 piezas**: `layout`, `catalog`, `model` y `year_overrides`.

1. Crear el layout anual.
   Archivo recomendado: `src/arrendatools/modelo303/infrastructure/layout_2027.py`.
   Puedes hacerlo a partir de `layout_2026.py` y ajustar orden de campos/páginas según el diseño oficial del año.

2. Registrar el layout en el registry.
   Edita `src/arrendatools/modelo303/infrastructure/layout_registry.py`:
   - importa `LAYOUT` del nuevo módulo;
   - añade la entrada `2027: LAYOUT_2027` en `LAYOUTS`.
   `get_generator(...)` usa este diccionario para decidir si un ejercicio está soportado.

3. Revisar `catalog.py` para campos nuevos o cambios de formato.
   Archivo: `src/arrendatools/modelo303/infrastructure/catalog.py`.
   - Si aparecen campos nuevos en el layout, deben existir en `FIELD_CATALOG`.
   - Si cambia longitud/tipo, actualiza `FieldDef(length, field_type, ...)`.
   - Para campos numéricos:
     - usa `scale_to_cents=True` cuando el valor representa importes monetarios;
     - usa `scale_to_cents=False` para códigos, flags, año, etc.
   - Si cambia una regla de validación de tipo, ajusta `_validate_type(...)`.

4. Revisar el modelo de dominio para asegurar que todos los campos se resuelven.
   Archivo: `src/arrendatools/modelo303/domain/model.py`.
   - Si el nuevo layout/catálogo introduce campos de datos (no literales), añade atributos en `Modelo303Model`.
   - Si el año exige lógica distinta en cálculos, intenta mantener los métodos base (`compute_casilla_*`) estables y delega diferencias anuales a overrides.
   - Mantén operaciones monetarias con `Decimal` y `quantize(...)`.

5. Crear y registrar overrides anuales.
   Crea `src/arrendatools/modelo303/infrastructure/year_overrides_2027.py` con:
   - `CASILLA_DEFAULTS`: valores simples por defecto para ese año;
   - `CASILLA_CALCULATORS`: funciones para campos cuyo cálculo cambia ese año.
   Luego registra el módulo en `src/arrendatools/modelo303/infrastructure/year_overrides.py`:
   - importa `CASILLA_DEFAULTS` y `CASILLA_CALCULATORS`;
   - añade `2027` en `YEAR_OVERRIDES_REGISTRY`.

6. Añadir tests del nuevo ejercicio.
   - Crea tests tipo `tests/test_generator_tax_year_2027.py` tomando como base los de 2026.
   - Añade ficheros golden en `tests/golden/2027/...`.
   - Actualiza tests de factoría/soporte de años (`tests/test_modelo303_factory.py`) para incluir 2027.
   - Verifica también los tests de alineación (`tests/test_catalog_model_alignment.py`), que detectan campos en layout sin catálogo o campos no renderizables.

Checklist mínimo para dar por soportado un nuevo año:

1. `get_generator(2027)` devuelve generador sin error.
2. Todos los campos de `layout_2027` existen en `FIELD_CATALOG`.
3. `Modelo303Model.from_data(...)` genera string válido para escenarios 1T/2T/3T, 4T y sin IBAN.
4. Golden tests del año pasan.

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
