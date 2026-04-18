from decimal import Decimal, ROUND_HALF_UP


def as_decimal(value: Decimal | int | float) -> Decimal:
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def to_cents(value: Decimal | int | float) -> int:
    number = as_decimal(value)
    rounded = number.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(rounded * Decimal("100"))


def format_signed_numeric(value: Decimal | int | float, length: int) -> str:
    cents = to_cents(value)
    magnitude = str(abs(cents)).zfill(length)
    if cents < 0:
        return "N" + magnitude[1:]
    return magnitude
