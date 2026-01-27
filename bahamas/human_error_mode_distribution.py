# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import numpy as np
import pandas as pd
from scipy.stats import lognorm
import logging

logger = logging.getLogger('BAHAMAS.HEMD')

from .utils import SDLC_stages, human_error_modes


def get_hemd_from_spreadsheet(spreadsheet_file, sheet_name="HEMD", distribution="lognorm"):
    """
    Parameters
    ----------
    spreadsheet_file : str
        Filename of the spreadsheet to read in
    sheet_name : str
        Name of the sheet with the human error mode distribution data
    distribution : str
        Type of distribution to use (currently only "lognorm" is supported)

    Returns
    -------
    hemd, dist_dict : dict, dict
        The first dictionary contains the rvs sampling function for the action
        type; the second dictionary contains the distribution dictionary --- both
        are keyed by the action type.

    gets the human error mode distributions from a spreadsheet
    """
    hemd = {}
    dist_dict = {}
    df = pd.read_excel(spreadsheet_file,sheet_name=sheet_name)
    for row in df.iterrows():
        series = row[1]
        # logger.info(f"{series.key} {series.sigma} {series.mu}")
        if distribution == "lognorm":
            dist = lognorm(s=series.sigma, scale=np.exp(series.mu))
        else:
            logger.error("Unsupported distribution type %s", distribution)
        dist_dict[series.key] = dist
        hemd[series.key] = dist.rvs
    return hemd, dist_dict
