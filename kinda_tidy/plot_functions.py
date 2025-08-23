import numpy as np
import pandas as pd
import plotnine as gg
from plotnine import *
from typing import List

import kinda_tidy


def create_plotting_data(domain: List, n:int=100, **funcs) -> pd.DataFrame:
    """Create plotting data for functions over a specified domain.

    Args:
        domain (List): A list containing the start and end of the domain [start, end].
        n (int, optional): Number of points to sample in the domain. Defaults to 100.
        **funcs: Arbitrary number of keyword arguments where the key is the function name
                  and the value is a callable that takes a scalar and returns a scalar.

    Returns:
        pd.DataFrame: A pandas dataframe with function values evaluated on a range.
    """
    if len(domain) != 2:
        raise ValueError("Domain must be a list of two elements: [start, end]")
    
    vf = {name: np.vectorize(func) for name, func in funcs.items()}
    df = pd.DataFrame({'_x':  np.linspace(domain[0], domain[1], n)})
    for name, func in vf.items():
        df[name] = func(df._x)

    return df
   
def plot_functions(domain: List, n:int=100, **funcs) -> gg.ggplot:
    """Plot functions over a specified domain.

    Args:
        domain (List): A list containing the start and end of the domain [start, end].
        n (int, optional): Number of points to sample in the domain. Defaults to 100.
        **funcs: Arbitrary number of keyword arguments where the key is the function name
                  and the value is a callable that takes a scalar and returns a scalar.

    Returns:
        gg.ggplot: A plotnine ggplot object with the plotted functions.
    """
    if len(domain) != 2:
        raise ValueError("Domain must be a list of two elements: [start, end]")
    
    df = create_plotting_data(domain, n, **funcs)


    p = (df
         .melt(id_vars='_x', var_name='function', value_name='y')
        .ggplot(gg.aes(x='_x', y='y', color='function'))
         + gg.geom_line()
         + labs(x='', y='')
         )
    return p
