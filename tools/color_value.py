try:
    import numpy as np
except ImportError:
    pass

import colorsys

__all__ = ['value_to_color']


def math_map(value, fromMin, fromMax, toMin, toMax):
    """
    Maps a value from one range to another.
    Arguments:
    ----------
    value : value to be mapped
    fromMin : lower bound of the value's current range
    fromMax : upper bound of the value's current range
    toMin : lower bound of the value's target range
    toMax : upper bound of the value's target range
    """
    delta = fromMax - fromMin
    if delta == 0 : return 0
    return toMin + ((toMax - toMin) / delta) * (value - fromMin)


def color_hue_to_rgb(hue):
    """
    Converts a color defined as Hue (HSV, saturation and value assumed to be 100%) into red, green and blue
    and returns (r,g,b,1)
    """
    col = colorsys.hsv_to_rgb(hue, 1, 1)
    return (col[0], col[1], col[2], 1)  # alpha = 100 %


def value_to_color(value_array, min_value, max_value, min_hue, max_hue):
    ndim = value_array.ndim
    new_shape = []
    for i in range(ndim):
        new_shape.append(value_array.shape[i])
    new_shape.append(4)
    new_shape = tuple(new_shape)
    color_array = np.empty((new_shape))
    with np.nditer(value_array, flags=['multi_index']) as it:
        for x in it:
            hue = math_map(
                x, min_value, max_value, min_hue, max_hue)
            color_array[it.multi_index] = color_hue_to_rgb(hue)
    return color_array