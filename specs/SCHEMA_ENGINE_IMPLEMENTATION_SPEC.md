# Especificación De Implementación: Engine + Schema AEAT Para Modelo 303

## 1. Propósito

Este documento define la especificación funcional y técnica para rediseñar el generador del Modelo 303 de forma que:

- el motor de generación sea estable y común;
- cada ejercicio o revisión de la AEAT se represente como un `schema` completo y autónomo;
- el `schema` pueda generarse automáticamente a partir del Excel oficial publicado por la AEAT;
- el alta de un nuevo ejercicio o revisión requiera principalmente importar un nuevo Excel, generar el `schema`, completar la lógica no inferible y ejecutar tests.

Este documento está pensado para servir como base de trabajo para una IA de desarrollo.

## 2. Contexto Actual

El repositorio actual implementa el Modelo 303 con estas piezas principales:

- un generador común;
- un `layout` anual escrito a mano;
- un catálogo global de campos;
- un modelo de dominio con cálculos y defaults comunes;
- overrides por ejercicio para diferencias pequeñas.

La solución actual funciona, pero añadir un ejercicio nuevo obliga a tocar varios puntos:

- `layout_YYYY.py`
- `layout_registry.py`
- `catalog.py`
- `domain/model.py`
- `year_overrides_YYYY.py`
- `year_overrides.py`
- tests y golden files

El objetivo del rediseño es reducir este acoplamiento.

## 3. Objetivo Del Rediseño

La arquitectura objetivo debe separar claramente:

1. motor estable de generación;
2. definiciones versionadas del formato oficial;
3. lógica de negocio común;
4. importación automática del diseño oficial desde Excel.

### Principio Principal

Cada ejercicio o revisión debe quedar representado por un `schema` completo y autosuficiente.

Se acepta explícitamente que los `schemas` anuales repitan mucha información. La prioridad es:

- simplicidad;
- trazabilidad frente al Excel oficial;
- aislamiento entre ejercicios;
- facilidad de eliminación de soporte de años antiguos.

No es necesario implementar herencia, deltas entre años ni capas de composición entre `schemas`.

## 4. Restricciones Y Preferencias

- La API pública actual debe mantenerse estable en la medida de lo posible.
- El repositorio seguirá soportando solo los últimos 2 años operativos.
- Aun así, los `schemas` históricos pueden permanecer en el repositorio como artefactos técnicos si son útiles.
- El Excel oficial de la AEAT será la fuente de verdad estructural.
- El engine no debe depender del Excel en tiempo de ejecución.
- El `schema` generado debe ser persistido en disco y versionado en Git.
- Se prefiere un diseño simple y explícito frente a uno muy abstracto.

## 5. Resultado Esperado

El sistema final debe permitir este flujo:

1. La AEAT publica un nuevo Excel.
2. Se guarda en `specs/<year>/...xlsx`.
3. Se ejecuta un generador/importador.
4. El generador produce un `schema` interno versionado.
5. El motor usa ese `schema` para generar el fichero final.
6. Se completan en código solo las reglas de negocio que no se puedan deducir del Excel.
7. Se ejecutan tests de validación y golden files.

## 6. Arquitectura Objetivo

La implementación debe converger hacia una arquitectura similar a esta:

```text
specs/
  2025/
    <excel oficial>
  2026/
    <excel oficial>

src/arrendatools/modelo303/
  application/
    data.py
    facade.py
    generator.py

  domain/
    model.py

  infrastructure/
    formatting.py
    schema_loader.py
    schema_validator.py
    schema_registry.py
    schema_renderer.py
    builtins.py
    schemas/
      2025.1.yaml
      2026.1.yaml
      ...

tools/
  import_aeat_excel.py
  compare_schemas.py
```

### Responsabilidad De Cada Pieza

#### `schema_loader.py`

Carga un `schema` YAML/JSON desde disco y lo convierte en estructuras internas tipadas.

#### `schema_validator.py`

Valida que el `schema` sea coherente antes de usarse:

- páginas válidas;
- campos válidos;
- tipos válidos;
- fuentes de valor válidas;
- posiciones y longitudes coherentes;
- referencias correctas;
- expresiones seguras.

#### `schema_registry.py`

Define qué ejercicios o revisiones están soportados operativamente.

Los `schemas` deben residir dentro de `src/arrendatools/modelo303/infrastructure/schemas/` o una ruta equivalente dentro del paquete distribuible, para que formen parte de la librería publicada en PyPI.

#### `schema_renderer.py`

Recorre páginas y campos del `schema`, resuelve el valor de cada campo y delega el formateo al motor existente.

#### `builtins.py`

Contiene funciones Python registradas para reglas que no conviene expresar como datos del `schema`.

#### `tools/import_aeat_excel.py`

Lee el Excel oficial de la AEAT y genera un `schema` interno.

#### `tools/compare_schemas.py`

Compara dos `schemas` y reporta diferencias estructurales.

## 7. Fuente Oficial: Excel AEAT

La AEAT publica cada versión del diseño de registro mediante un Excel.

Ejemplo real de entrada:

- `specs/2026/20260128 - DR303e26v101.xlsx`

Este Excel tiene una hoja por bloque/página, por ejemplo:

- `DP30300`
- `DP30301`
- `DP30302`
- `DP30303`
- `DP30304`
- `DP30305`
- `DP303DID`

Y las hojas contienen columnas como:

- `Nº`
- `Posic.`
- `Lon`
- `Tipo`
- `Descripción`
- `Validación`
- `Contenido`
- en algunos casos `Comp`

### Decisión De Diseño

El Excel oficial es la fuente de verdad del formato, pero no debe ser consumido directamente por el engine.

Debe existir una fase de importación:

`Excel AEAT -> Schema interno del proyecto`

El Excel oficial puede vivir en `specs/` como artefacto de trabajo y trazabilidad, pero el `schema` final consumible por la librería debe quedar dentro de `src`.

## 8. Formato Del Schema

El formato recomendado del `schema` es YAML por legibilidad y facilidad de revisión en Git.

Cada `schema` debe ser completo y autosuficiente.

### Requisitos Del Schema

Cada `schema` debe contener como mínimo:

- identificador del schema;
- ejercicio fiscal;
- revisión o versión;
- fecha de la especificación;
- referencia al fichero Excel origen;
- lista de páginas;
- lista ordenada de campos por página;
- para cada campo:
  - nombre lógico;
  - posición;
  - longitud;
  - tipo;
  - origen del valor;
  - valor literal o referencia cuando aplique;
  - descripción;
  - validación;
  - metadata descriptiva opcional.

### Estructura Conceptual Mínima

```yaml
schema_id: "modelo303-2026.1"
fiscal_year: 2026
revision: "1.01"
specification_date: "2026-01-28"
source_file: "specs/2026/20260128 - DR303e26v101.xlsx"

pages:
  - id: "DP30300"
    include_when: "always"
    fields:
      - name: "registro_general_open"
        position: 1
        length: 2
        field_type: "alphanumeric"
        source: "constant"
        value: "<T"
        description: "Constante."
        validation: ""
      - name: "modelo"
        position: 3
        length: 3
        field_type: "numeric"
        source: "constant"
        value: "303"
        description: "Modelo"
        validation: ""
```

No es necesario que la primera implementación soporte todas las posibles variantes. Debe cubrir primero los casos reales del repositorio actual.

## 9. Tipos De Campo

El `schema` debe soportar al menos estos tipos internos:

- `alphabetical`
- `alphanumeric`
- `numeric`
- `numeric_signed`

Estos tipos deben mapearse a la lógica ya existente de formateo y validación.

## 10. Orígenes Del Valor De Un Campo

El `schema` debe soportar al menos estos `source`:

- `constant`
- `default`
- `model`
- `builtin`
- `formula`

### Significado

#### `constant`

Campo con valor fijo literal definido en el `schema`.

Ejemplos:

- `"<T"`
- `"303"`
- `"01000"`
- `">"`

#### `default`

Campo cuyo valor por defecto se define en el `schema`, pero conceptualmente forma parte del dato de negocio o del modelo anual.

Ejemplos:

- blancos;
- ceros;
- tipos porcentuales por defecto;
- casillas con valores fijos del ejercicio.

#### `model`

Campo cuyo valor se obtiene de un atributo del modelo de dominio ya calculado.

Ejemplos:

- `ejercicio`
- `periodo`
- `nif`
- `casilla_07`

#### `builtin`

Campo cuyo valor se resuelve llamando a una función Python registrada.

Ejemplos adecuados:

- `tipo_declaracion`
- `exencion_390`
- `operaciones_no_cero`
- `marca_sepa`

#### `formula`

Campo cuya expresión se puede resolver a partir de otros campos o atributos mediante una fórmula simple y segura.

Ejemplos adecuados:

- sumas/restas de casillas;
- multiplicaciones o divisiones sencillas;
- dependencias aritméticas directas.

## 11. Qué Debe Importarse Automáticamente Del Excel

El importador del Excel debe extraer, como mínimo:

- fecha de la especificación, cuando sea deducible del nombre del fichero o de metadatos fiables asociados;
- nombre de página o bloque;
- orden de páginas;
- orden de campos;
- posición;
- longitud;
- tipo;
- descripción;
- validación;
- contenido literal cuando sea claramente una constante;
- indicaciones de campos en blanco o reservados;
- posibles marcas de complementaria si aparecen de forma estructurada.

### Requisito Sobre La Descripción

El `schema` generado debe contener obligatoriamente un campo `description` para cada campo importado.

Ese `description` debe incorporar la descripción proporcionada por el Excel oficial de la AEAT, con la menor transformación posible compatible con la normalización del formato.

La descripción no es opcional en el `schema` generado desde Excel.

### Requisito Sobre La Validación

El `schema` generado debe contener un campo `validation` para cada campo importado.

Ese `validation` debe incorporar el contenido de la columna de validación del Excel oficial de la AEAT, preservando la información original en la mayor medida posible.

Si una fila no contiene validación explícita, el valor podrá ser cadena vacía, pero la clave `validation` debe existir igualmente en el `schema` generado.

### Requisito Sobre La Fecha De La Especificación

El `schema` debe incluir un metadato obligatorio `specification_date`.

Ese valor debe representar la fecha de la especificación oficial de la AEAT a la que corresponde el `schema`.

Cuando sea posible, el importador debe obtenerla automáticamente a partir de:

- el nombre del fichero Excel;
- metadatos fiables asociados;
- otra fuente estructurada y verificable disponible durante la importación.

Si no pudiera inferirse automáticamente de forma fiable, el importador debe permitir pasarla como parámetro explícito y debe fallar o emitir una advertencia clara si ese dato obligatorio no se resuelve.

### Reglas De Mapeo Inicial

#### Columna `Tipo`

Debe mapearse aproximadamente así:

- `A` o `An` -> `alphabetical` o `alphanumeric` según contexto;
- `Num` -> `numeric`;
- `N` -> `numeric_signed`.

La implementación debe documentar y centralizar este mapeo para poder corregirlo si en algún Excel aparece una variante distinta.

#### Columna `Contenido`

Debe analizarse para detectar estos casos:

- `Constante "..."` -> `source = constant`
- `BLANCOS` o `En blanco` -> `source = default`, `value = " "`
- referencias a notas o reglas no directamente ejecutables -> almacenar como metadata, no inferir lógica automática arriesgada

#### Posición Y Longitud

Deben copiarse literalmente al `schema`.

## 12. Qué No Debe Inferirse Automáticamente Del Excel

El importador no debe intentar deducir automáticamente reglas complejas de negocio a partir de texto libre del Excel o de notas ambiguas.

No debe intentar inferir automáticamente:

- fórmulas complejas de casillas;
- semántica tributaria no explícita;
- condiciones lógicas complejas;
- comportamiento condicional derivado de notas interpretativas;
- decisiones de negocio ya codificadas hoy en `domain/model.py`.

Esas reglas deben mantenerse en Python hasta que exista una representación declarativa clara y segura.

## 13. Builtins Python

Debe existir un registro explícito de funciones Python permitidas para resolver campos no triviales.

Ejemplos de builtins iniciales esperables:

- `declaration_type`
- `exoneracion_modelo_390`
- `operaciones_no_cero`
- `marca_sepa`

Opcionalmente, más adelante:

- `amount`
- otras reglas comunes que merezca la pena centralizar

### Requisitos

- El `schema` solo puede invocar builtins registradas.
- No se permitirá ejecutar código arbitrario desde el `schema`.

## 14. Fórmulas

La primera versión del motor puede soportar fórmulas simples.

### Requisitos

- Solo permitir operadores seguros y conocidos.
- No usar `eval` sobre expresiones arbitrarias.
- Implementar un evaluador restringido o un parser seguro.

### Operadores Iniciales Permitidos

- `+`
- `-`
- `*`
- `/`
- paréntesis

### Operandos Permitidos

- referencias a atributos/campos del modelo;
- literales numéricos simples.

### Ejemplos Adecuados

- `casilla_69 - casilla_70 + casilla_109`
- `(casilla_64 * casilla_65) / 100`

## 15. Modelo De Dominio

`Modelo303Data` y `Modelo303Model` deben reutilizarse en la medida de lo posible.

### Decisión

La construcción base del modelo seguirá ocurriendo en Python:

- carga de datos de entrada;
- defaults comunes;
- normalizaciones iniciales;
- reglas generales de negocio;
- cálculos comunes ya existentes.

El `schema` no sustituye completamente al modelo de dominio. El `schema` define el formato oficial y el origen de cada campo.

El modelo de dominio sigue representando el estado calculado del Modelo 303.

### Requisito Sobre Cantidades Monetarias

Siempre que un valor represente una cantidad monetaria, debe usarse `Decimal` en la implementación interna.

Esto aplica, como mínimo, a:

- atributos monetarios del modelo;
- resultados de builtins monetarias;
- resultados de fórmulas monetarias;
- valores por defecto monetarios definidos en el `schema`;
- cualquier cálculo intermedio o final relacionado con importes.

No deben usarse `float` ni conversiones implícitas a coma flotante para cantidades monetarias.

## 16. Motor De Renderizado

El motor debe seguir esta secuencia:

1. Resolver el `schema` activo para el ejercicio solicitado.
2. Construir el `Modelo303Model` a partir de `Modelo303Data`.
3. Recorrer páginas en el orden del `schema`.
4. Evaluar `include_when` a nivel de página.
5. Recorrer campos en el orden del `schema`.
6. Evaluar `include_when` a nivel de campo si existe.
7. Resolver el valor según `source`.
8. Formatear el campo usando la lógica existente de tipos/longitudes.
9. Concatenar el resultado final.

## 17. Registro De Schemas Soportados

Debe existir un registro explícito de `schemas` soportados operativamente.

Ejemplo conceptual:

```python
SUPPORTED_SCHEMAS = {
    2025: "arrendatools/modelo303/infrastructure/schemas/2025.1.yaml",
    2026: "arrendatools/modelo303/infrastructure/schemas/2026.1.yaml",
}
```

Este registro:

- es la fuente de verdad de los años soportados;
- debe ser el único punto que cambia al retirar soporte operativo de un año;
- no obliga a borrar `schemas` históricos del repositorio.

## 18. Generador Del Schema A Partir Del Excel

Debe implementarse una herramienta de línea de comandos en:

- `tools/import_aeat_excel.py`

### Objetivo

Convertir el Excel oficial de la AEAT en un `schema` interno del proyecto.

### Entrada

- ruta al Excel oficial;
- opcionalmente año;
- opcionalmente revisión;
- ruta de salida del `schema`.

### Salida

- fichero YAML persistido en disco;
- opcionalmente un resumen por consola con:
  - páginas detectadas;
  - número de campos por página;
  - constantes detectadas;
  - advertencias;
  - elementos que requieren revisión manual.

### Comportamiento Esperado

El importador debe:

1. abrir el `.xlsx`;
2. recorrer hojas válidas;
3. localizar la fila de cabecera;
4. detectar columnas relevantes;
5. convertir cada fila de campo a una definición interna;
6. ignorar filas vacías o puramente decorativas;
7. generar un `schema` completo;
8. guardar el YAML;
9. emitir advertencias cuando no pueda inferir un valor de forma segura.

### Requisitos De Robustez

El importador debe tolerar:

- espacios extra en celdas;
- variaciones menores en nombres de columnas;
- hojas con celdas decorativas;
- contenido combinado o parcialmente vacío;
- notas y texto auxiliar que no correspondan a un campo real.

### Revisión Manual Esperada

Tras importar, puede ser necesario revisar manualmente:

- mapeos de tipo ambiguos;
- condiciones de visibilidad;
- builtins a usar;
- fórmulas complejas;
- nombres lógicos internos de ciertos campos.

El flujo de trabajo acepta esta revisión manual.

## 19. Comparador De Schemas

Debe implementarse una herramienta:

- `tools/compare_schemas.py`

### Objetivo

Comparar dos `schemas` y detectar diferencias estructurales.

### Debe Reportar Como Mínimo

- páginas añadidas/eliminadas;
- campos añadidos/eliminados;
- cambios de posición;
- cambios de longitud;
- cambios de tipo;
- cambios de `source`;
- cambios de constantes o defaults.

Esta herramienta será útil al incorporar un nuevo Excel anual o una revisión menor.

## 20. Validación Del Schema

El validador debe comprobar, como mínimo:

- no hay páginas duplicadas;
- no hay campos duplicados dentro de una página;
- `position` es entero positivo;
- `length` es entero positivo;
- `field_type` es válido;
- `source` es válido;
- si `source == constant` o `default`, existe `value`;
- si `source == model`, existe `attr`;
- si `source == builtin`, existe `function`;
- si `source == formula`, existe `expr`;
- referencias de builtins válidas;
- expresiones seguras y parseables;
- orden y coherencia estructural.

## 21. Compatibilidad Con La API Actual

Debe mantenerse, salvo imposibilidad justificada:

- `get_generator(fiscal_year)`
- `Modelo303Generator.generate(data)`
- `Modelo303Data`

El cambio interno deseado es:

- hoy `get_generator()` resuelve un `layout`;
- tras el rediseño `get_generator()` debe resolver un `schema`.

La API pública no debe volverse más compleja para el usuario final.

## 22. Criterios De Aceptación

Se considerará completado el rediseño cuando se cumpla lo siguiente:

1. Existe un `schema` por ejercicio/revisión soportado.
2. El generador usa el `schema` como fuente de verdad estructural.
3. El `schema` puede generarse a partir del Excel oficial mediante una herramienta reproducible.
4. Los tests existentes siguen pasando, o se sustituyen por tests equivalentes con la nueva arquitectura.
5. Los golden files generados coinciden con los actuales para los escenarios ya soportados.
6. El alta de un ejercicio nuevo requiere:
   - guardar el Excel;
   - ejecutar el importador;
   - revisar manualmente la parte no inferible;
   - ejecutar tests.

### Regla De Conservación De Tests

Si la API pública se mantiene, los tests actuales no deben cambiar salvo adaptación mínima estrictamente necesaria por reorganización interna.

En particular:

- deben conservarse los tests funcionales existentes siempre que sigan representando el mismo contrato público;
- no deben cambiarse los golden files actuales salvo que exista una razón funcional real y justificada;
- un rediseño interno no es motivo suficiente para modificar los resultados esperados.

Si fuera imprescindible tocar algún test, debe justificarse explícitamente y preservar el comportamiento público de la librería.

## 23. No Objetivos

No es objetivo de esta primera iteración:

- modelar todas las reglas tributarias del 303 exclusivamente en YAML;
- eliminar por completo `Modelo303Model`;
- deduplicar `schemas` entre años;
- construir un DSL complejo o muy genérico;
- soportar todos los posibles modelos AEAT distintos del 303.

## 24. Recomendaciones De Implementación Para La IA

- Priorizar cambios pequeños y verificables.
- Reutilizar el código existente de formateo y dominio siempre que sea razonable.
- No intentar inferir lógica fiscal compleja desde texto libre del Excel.
- Mantener el engine simple y predecible.
- Favorecer trazabilidad y claridad antes que abstracciones avanzadas.
- Añadir tests junto con cada fase relevante.

## 25. Entregables Esperados

La implementación final debe incluir, como mínimo:

- estructuras internas de `schema`;
- loader y validator;
- renderer basado en `schema`;
- registry de `schemas` soportados;
- builtins registradas;
- importador de Excel a schema;
- comparador de schemas;
- tests;
- documentación mínima de uso.

## 26. Resumen Ejecutivo

La decisión central es esta:

- el Excel AEAT es la fuente de verdad del formato;
- el proyecto lo transforma a un `schema` interno completo y autónomo;
- el engine usa ese `schema`;
- la lógica fiscal compleja sigue en Python;
- los `schemas` anuales pueden repetirse sin problema;
- los `schemas` distribuidos por la librería deben vivir dentro de `src` para incluirse en PyPI;
- si la API pública no cambia, los tests y especialmente los golden files deben mantenerse estables;
- añadir un año nuevo debe ser una operación principalmente de importación y validación, no de reescritura manual del motor.
