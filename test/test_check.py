"""
Tests for check.py
"""
import numpy as np
from check import main


def test_main():
    """
    Testing main function of check.py
    """
    result = main()
    assert len(result) == 6
    assert np.array_equal(
        result.iloc[:, 1].values,
        np.array([245.00, 355.25, 461.50, 416.75, 334.75, 338.75]),
    )
    assert np.array_equal(
        result.iloc[:, 2].values, np.array([237.25, 185.25, 81, 97.25, 65.75, 172])
    )
