

import numpy as np
import hypothesis as hp
import hypothesis.strategies as st


# %% Strategies generator tests
@st.composite
def getNumpyArray(draw, *dim, min_value=0, max_value=1):
    """
    Generate a numpy array of float values.

    Parameters
    ----------
    *dim : *int
        The array shape.
    min_value : float, optional
        The minimum value of the data. The default is 0.
    max_value : TYPE, optional
        The maximum value of the data. The default is 1.

    Returns
    -------
    data : array
        An array of float data.

    """
    size = 1
    for n in dim:
        size *= n
    data = draw(st.lists(st.floats(min_value=min_value, max_value=max_value,
                                   exclude_max=True),
                         min_size=size, max_size=size))
    data = np.array(data).reshape(*dim)
    return data


# %% Strategies generator tests
@hp.given(data=st.data(),
          shape=st.lists(st.integers(min_value=1, max_value=1000),
                         min_size=1, max_size=3))
def test_getNumpyArray(data, shape):
    """
    Test getNumpyArray generator function.

    """
    array = data.draw(getNumpyArray(*shape))
    assert isinstance(array, type(np.array([])))
    assert array.shape == tuple(shape)
    assert np.max(array) <= 1
    assert np.min(array) >= 0
