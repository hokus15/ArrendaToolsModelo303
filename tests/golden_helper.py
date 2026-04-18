"""Helper utilities for golden file testing."""

from pathlib import Path


def get_golden_dir() -> Path:
    """Get the base golden files directory."""
    return Path(__file__).parent / "golden"


def load_golden(tax_year: int, scenario: str) -> str:
    """Load expected output from golden file.

    Parameters
    ----------
    tax_year : int
        Tax year (e.g., 2025, 2026).
    scenario : str
        Scenario name (e.g., '1T/positive', '2T3T/negative', '4T', 'without_iban').

    Returns
    -------
    str
        Expected output string.

    Raises
    ------
    FileNotFoundError
        If golden file doesn't exist.

    """
    golden_path = get_golden_dir() / str(tax_year) / scenario / "expected.txt"
    if not golden_path.exists():
        raise FileNotFoundError(
            f"Golden file not found: {golden_path}\n"
            f"Available scenarios for {tax_year}: {list_scenarios(tax_year)}"
        )
    return golden_path.read_text(encoding="utf-8")


def save_golden(tax_year: int, scenario: str, content: str) -> None:
    """Save output to golden file.

    Parameters
    ----------
    tax_year : int
        Tax year (e.g., 2025, 2026).
    scenario : str
        Scenario name (e.g., '1T/positive', '2T3T/negative', '4T', 'without_iban').
    content : str
        Content to save.

    """
    golden_path = get_golden_dir() / str(tax_year) / scenario / "expected.txt"
    golden_path.parent.mkdir(parents=True, exist_ok=True)
    golden_path.write_text(content, encoding="utf-8")


def list_scenarios(tax_year: int) -> list[str]:
    """List all available scenarios for a tax year."""
    year_dir = get_golden_dir() / str(tax_year)
    if not year_dir.exists():
        return []
    return [d.name for d in year_dir.iterdir() if d.is_dir()]
