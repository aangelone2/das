"""Compute simple average of a dataset by columns."""


import numpy as np

from common import MAXBINS
from common import drop_rows
from common import rebin
from common import get_stats


def avs(
    ds: np.array, skip_perc: float, power2: bool, verbose: bool
) -> None:
    """Compute simple average of a dataset by columns.

    Parameters
    -----------------------
    ds : np.array
        The dataset to parse
    skip_perc : float
        The percentage of rows to skip
    power2 : bool
        If True, skips additional rows to remain with a power
        of 2 of rows
    verbose : bool
        Prints additional information on the dataset
    """
    rows = ds.shape[0]

    ds = drop_rows(ds, skip_perc, power2)
    keep = ds.shape[0]

    bins = MAXBINS if power2 else keep
    ds = rebin(ds, bins)

    if verbose:
        print(f"{keep}/{rows} rows")
        print(f":: {bins} bins")
    print()

    stats = get_stats(ds)
    for scol in stats:
        print(f"{scol['m']:.11f}  ")
        print(f"{scol['s']:.4e}  ")
        print(f"{scol['ds']:.2e}")
