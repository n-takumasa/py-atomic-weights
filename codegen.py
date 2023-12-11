import datetime
from pathlib import Path

import pandas as pd
import polars as pl
import tomllib

table = (
    pd.read_html("https://iupac.qmul.ac.uk/AtWt/", header=0)[1]
    .pipe(pl.from_pandas)
    .with_columns(
        # r"\s+" : spaces between digits
        # r"\(\d+\)" : uncertainty
        # r"\[|\]" : radioactive elements
        pl.col("Atomic Wt").str.replace_all(r"(\s+|\(\d+\)|\[|\])", ""),
    )
)

code_float = (
    table.select(
        pl.col("At No"),
        expr=pl.col("Symbol") + " = " + pl.col("Atomic Wt"),
    )
    .sort("At No")
    .pipe(lambda x: "\n".join(x.get_column("expr")))
)

code_decimal = (
    table.select(
        pl.col("At No"),
        expr=pl.col("Symbol") + ' = Decimal("' + pl.col("Atomic Wt") + '")',
    )
    .sort("At No")
    .pipe(lambda x: "\n".join(x.get_column("expr")))
)

cwd = Path(__file__).parent

with (cwd / "pyproject.toml").open("rb") as f:
    version = tomllib.load(f)["tool"]["poetry"]["version"]

with (cwd / "atomic_weights/__init__.py").open("w") as f:
    f.write(
        f"""
# ruff: noqa
# generated at {datetime.datetime.now(datetime.UTC)}

__version__ = "{version}"
from . import _decimal as decimal

{code_float}
"""[1:]
    )

with (cwd / "atomic_weights/_decimal.py").open("w") as f:
    f.write(
        f"""
# ruff: noqa
# generated at {datetime.datetime.now(datetime.UTC)}

from decimal import Decimal

{code_decimal}
"""[1:]
    )
