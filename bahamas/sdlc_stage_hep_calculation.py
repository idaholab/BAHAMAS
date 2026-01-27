# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import numpy as np
import pandas as pd
from scipy.stats import lognorm
import logging
from . import human_error_mode_distribution

logger = logging.getLogger('BAHAMAS.HEP')

def sdlc_stage_hep_calculation(excel_file_path, sheet_name, hemd, num_samples=100, distribution="lognorm"):
    """
    Parameters
    ----------
    excel_file_path : str
        Filename of the spreadsheet with the number of actions and types
    sheet_name : str
        Sheet name in the spreadsheet with the data
    hemd : dict
        Dictionary of rvs functions, keyed by action type
    num_samples : int
        Number of samples to generate for each action
    distribution : str
        Type of distribution to use (currently always "lognorm")

    Returns
    -------
    total, fitted : numpy.array, dict
        The samples for the SDLC stage by considering all human error propagations,
        and a dictionary of the fitted mu and sigma parameters.

    This function reads in the number of human actions and human error modes from a
    spreadsheet, and calculates the human error probability distributions.
    """
    logger.info('Calculate SDLC "%s" stage HEP', sheet_name)
    # Read the action types from the given sheet
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, usecols=["Task Number","Human Error Mode"])
    df = df.dropna()
    num_actions = df.iloc[:, 0].to_numpy()
    action_types = df.iloc[:, 1].to_numpy()

    # change to bounded method to avoid the explosion of total distribution
    action_samples = np.array([hemd[action_types[i]].rvs(num_samples) for i in range(len(num_actions))])
    total = 1 - np.prod(1-action_samples, axis=0)

    stage_mean = np.mean(total)
    # Fit the lognormal distribution to the total samples
    if distribution == "lognorm":
        shape, loc, scale = lognorm.fit(total, floc=0)
        fitted = {
            'mu': np.log(scale),
            'sigma': shape,
            'mean' : np.mean(total),
            'median' : np.median(total),
            'std' : np.std(total)
        }
    else:
        raise IOError("Unsupported distribution type %s", distribution)

    return total, fitted
