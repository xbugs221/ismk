import numpy as np
import polars as pl
import pandas as pd

assert isinstance(ismk.params.testnp, np.ndarray)
assert isinstance(ismk.params.testpl, pl.DataFrame)
assert isinstance(ismk.params.testpd, pd.DataFrame)

ismk.params.testpd.to_csv(ismk.output.pd, sep="\t")
ismk.params.testpl.write_csv(ismk.output.pl, separator="\t")
np.savetxt(ismk.output.np, ismk.params.testnp, delimiter="\t")