from __future__ import annotations


def some_function(data: str, prefixes: list[str] | None = None) -> str:
    for prefix in prefixes:
        data = f"{prefix}_{data}"
    return data
