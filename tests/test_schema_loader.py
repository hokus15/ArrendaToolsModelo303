"""Tests for schema_loader.py."""

import textwrap
from pathlib import Path

from arrendatools.modelo303.infrastructure.schema import FieldType, Source
from arrendatools.modelo303.infrastructure.schema_loader import load_schema


def _write_yaml(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "schema.yaml"
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


MINIMAL_SCHEMA_YAML = """\
schema_id: "modelo303-test"
fiscal_year: 2099
revision: "1.00"
specification_date: "2099-01-01"
source_file: "specs/test.xlsx"
pages:
  - id: test_page
    include_when: always
    fields:
      - id: test_page_1
        name: field_const
        position: 1
        length: 3
        field_type: alphanumeric
        source: constant
        value: "303"
        metadata:
          tipo: AN
          descripcion: "El modelo."
          validacion: ""
          contenido: ""
      - id: test_page_2
        name: field_model
        position: 4
        length: 17
        field_type: numeric_signed
        source: model
        metadata:
          tipo: N
          descripcion: "Una casilla."
          validacion: ""
          contenido: ""
      - id: test_page_3
        name: field_formula
        position: 21
        length: 17
        field_type: numeric_signed
        source: formula
        expr: "casilla_69 - casilla_70"
        metadata:
          tipo: N
          descripcion: "Calculada."
          validacion: ""
          contenido: ""
"""


def test_load_schema_metadata(tmp_path):
    path = _write_yaml(tmp_path, MINIMAL_SCHEMA_YAML)
    schema = load_schema(path)

    assert schema.schema_id == "modelo303-test"
    assert schema.fiscal_year == 2099
    assert schema.revision == "1.00"
    assert schema.specification_date == "2099-01-01"
    assert schema.source_file == "specs/test.xlsx"


def test_load_schema_pages(tmp_path):
    path = _write_yaml(tmp_path, MINIMAL_SCHEMA_YAML)
    schema = load_schema(path)

    assert len(schema.pages) == 1
    page = schema.pages[0]
    assert page.id == "test_page"
    assert page.include_when == "always"


def test_load_schema_fields_count(tmp_path):
    path = _write_yaml(tmp_path, MINIMAL_SCHEMA_YAML)
    schema = load_schema(path)

    assert len(schema.pages[0].fields) == 3


def test_load_schema_constant_field(tmp_path):
    path = _write_yaml(tmp_path, MINIMAL_SCHEMA_YAML)
    schema = load_schema(path)
    f = schema.pages[0].fields[0]

    assert f.field_id == "test_page_1"
    assert f.name == "field_const"
    assert f.position == 1
    assert f.length == 3
    assert f.field_type == FieldType.ALPHANUMERIC
    assert f.source == Source.CONSTANT
    assert f.value == "303"
    assert f.metadata.descripcion == "El modelo."
    assert f.metadata.validacion == ""


def test_load_schema_model_field(tmp_path):
    path = _write_yaml(tmp_path, MINIMAL_SCHEMA_YAML)
    schema = load_schema(path)
    f = schema.pages[0].fields[1]

    assert f.field_id == "test_page_2"
    assert f.name == "field_model"
    assert f.source == Source.MODEL


def test_load_schema_formula_field(tmp_path):
    path = _write_yaml(tmp_path, MINIMAL_SCHEMA_YAML)
    schema = load_schema(path)
    f = schema.pages[0].fields[2]

    assert f.field_id == "test_page_3"
    assert f.name == "field_formula"
    assert f.source == Source.FORMULA
    assert f.expr == "casilla_69 - casilla_70"


def test_load_schema_from_traversable(tmp_path):
    """load_schema should accept objects with a read_text() method."""
    content = textwrap.dedent(MINIMAL_SCHEMA_YAML)

    class FakeTraversable:
        def read_text(self, encoding="utf-8"):
            return content

    schema = load_schema(FakeTraversable())
    assert schema.fiscal_year == 2099


def test_load_schema_empty_pages(tmp_path):
    yaml_content = """\
schema_id: "minimal"
fiscal_year: 2099
revision: "1.00"
specification_date: "2099-01-01"
source_file: ""
pages: []
"""
    path = _write_yaml(tmp_path, yaml_content)
    schema = load_schema(path)
    assert schema.pages == ()


def test_load_real_2025_schema():
    from arrendatools.modelo303.infrastructure.schema_registry import get_schema

    schema = get_schema(2025)
    assert schema.fiscal_year == 2025
    assert len(schema.pages) > 0


def test_load_real_2026_schema():
    from arrendatools.modelo303.infrastructure.schema_registry import get_schema

    schema = get_schema(2026)
    assert schema.fiscal_year == 2026
    assert len(schema.pages) > 0
