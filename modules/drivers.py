"""High-level drivers using the basic functions.

Functions
-----------------------
avs()
    Compute simple average of a dataset by columns.
"""


import numpy as np

from modules.common import drop_rows
from modules.common import get_stats


def avs(
    ds: np.array, skip_perc: float
) -> (list[dict[str, float]], str):
    """Compute simple average of a dataset by columns.

    Parameters
    -----------------------
    ds : np.array
        The dataset to parse
    skip_perc : float
        The percentage of rows to skip

    Returns
    -----------------------
    (list[dict[str, float]], str)
        - (mean, std, error on std) for each column (keys: (m, s, ds))
        - String carrying additional information
    """
    rows = ds.shape[0]

    ds = drop_rows(ds, skip_perc, power2=False)
    keep = ds.shape[0]

    report = f"{keep}/{rows} rows :: {keep} bins"

    stats = get_stats(ds)
    for col_res in stats:
        del col_res["sum"]

    return (stats, report)
