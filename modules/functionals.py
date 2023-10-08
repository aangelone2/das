"""Functionals to be used as arguments in drivers such as `jck`.

To be passed as a functional to `jck`, a function should have
the following features:
    - Be valid for either floating-point arguments or numpy
      arrays of floating points.
    - Be defined in terms of mean values of quantities.

Functions
-----------------------
susceptibility()
    Computes `a1 - a2^2`, where `a1` and `a2` are its
    (mean value) arguments.
"""


from typing import Union
import numpy as np


def susceptibility(
    x1: Union[float, np.array], x2: Union[float, np.array]
) -> Union[float, np.array]:
    """Susceptibility function for jackknife estimates.

    Returns (x1 - (x2)^2).

    Parameters
    -----------------------
    x1, x2 : Union[float, np.array]
        Input data (may be single numbers or arrays)

    Returns
    -----------------------
    Union[float, np.array]
        The computed susceptibilities.
    """
    return x1 - x2**2.0
