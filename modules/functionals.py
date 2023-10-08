"""Functionals to be used as arguments in drivers such as `jck`.

To be passed as a functional to `jck`, a function should have
the following features:
    - Receive as arguments a list of floating-point or numpy
      arrays.
    - Be defined in terms of mean values of quantities.
    - Check the length of the passed list, and raise a
      TypeError in case the number of arguments is invalid.

Functions
-----------------------
susceptibility()
    Computes `l[0] - l[1]^2`, where `l` is the passed argument
    list.
"""


from typing import Union
import numpy as np


def susceptibility(
    args: list[Union[float, np.array]]
) -> Union[float, np.array]:
    """Susceptibility function for jackknife estimates.

    Returns (args[0] - (args[1])^2).

    Parameters
    -----------------------
    args : list[Union[float, np.array]]
        Input data (may be single numbers or arrays).

    Returns
    -----------------------
    Union[float, np.array]
        The computed susceptibilities.

    Raises
    -----------------------
    TypeError
        If invalid length of the passed list.
    """
    if len(args) != 2:
        raise TypeError(
            "invalid number of arguments in susceptibility()"
        )
    return args[0] - args[1] ** 2.0
