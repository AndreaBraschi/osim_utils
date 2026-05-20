import math
import numpy as np
from numpy import array

from numpy import ndarray
from pandas import DataFrame, Series, Index


def Rx(angle: float) -> ndarray:
    cos, sin = math.cos(angle), math.sin(angle)

    mat: ndarray = array([
        [1, 0, 0],
        [0, cos, -sin],
        [0, sin, cos]
    ])

    return mat


def Ry(angle: float) -> ndarray:
    cos, sin = math.cos(angle), math.sin(angle)

    mat: ndarray = array([
        [cos, 0, sin],
        [0, 1, 0],
        [-sin, 0, cos]
    ])

    return mat


def Rz(angle: float) -> ndarray:
    cos, sin = math.cos(angle), math.sin(angle)

    mat: ndarray = array([
        [cos, -sin, 0],
        [sin, cos, 0],
        [0, 0, 1]
    ])

    return mat

QUALYSIS_TO_OPENSIM = Rz(-math.pi / 2) @ Ry(-math.pi / 2)