"""Common utilities, used by several higher-level scripts.

Functions
-----------------------
parse_ds()
    Parse a 2D data set from a file.
"""


import numpy as np


# MAX AND MIN NUM OF BINS TO CONSIDER WHEN BINNING
MAXBINS = 1024
MINBINS = 64


def parse_df(
    file: str,
    fields: list[int] | None = None,
    colnum_test: bool = False,
) -> np.array:
    """Parse a 2D data set from a file.

    Ignores blank lines, does not accept non-commented headers.
    Raises error if empty column read.

    Parameters
    -----------------------
    file : str
        The file to open for reading
    fields : list[int] | None, default = None
        List of fields to parse (0-indexed), all fields if None
    colnum_test: bool, default = False
        If True, checks if all rows have the same number of columns

    Returns
    -----------------------
    np.array
        A 2D array with the parsed dataset

    Raises
    -----------------------
    FIXME
    """
    # FIXME exceptions

    if not colnum_test:
        # only take selected columns, others ignored
        # (unless an empty column in or between the selected,
        # then an exception is raised)
        dataset = np.loadtxt(
            file,
            comments="#",
            dtype=np.float64,
            usecols=fields,
        )
        # FIXME exception
        # FIXME field not found
    else:
        # get all columns
        dataset = np.loadtxt(
            file, comments="#", dtype=np.float64, usecols=None
        )

        if fields is not None:
            dataset = dataset[:, fields]

    if len(dataset.shape) == 1:
        dataset = dataset.reshape(dataset.shape[0], 1)

    return dataset
