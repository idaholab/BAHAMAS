# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import numpy as np
import pandas as pd
from scipy.stats import lognorm, norm, truncnorm
import logging

logger = logging.getLogger('BAHAMAS.HEPApprox')

def sdlc_stage_hep_calculation_approx(excel_file_path, sheet_name, num_samples=100, distribution="norm"):
    """
    This function reads in the human error probability (mean and std) from a
    spreadsheet and calculates the human error probability distributions.

    Parameters
    ----------
    excel_file_path : str
        Filename of the spreadsheet with the number of actions and types
    sheet_name : str
        Sheet name in the spreadsheet with the data
    num_samples : int
        Number of samples to generate for each action
    distribution : str
        Type of distribution to use (currently always "norm")

    Returns
    -------
    total, None : numpy.array, None
        Samples for the SDLC stage by considering all human error propagations
    """
    logger.info('Calculate SDLC "%s" stage HEP', sheet_name)
    # Read the action types from the given sheet
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, usecols=["Human Error Probability (Mean)","Human Error Probability (STD)"])
    df = df.dropna()
    if df.empty:
        logger.error('Try to process %s, but got empty inputs!', excel_file_path)
        raise IOError(f'Try to process {excel_file_path}, but got empty inputs !')
    mean, std = df.iloc[0, 0], df.iloc[0, 1]

    if distribution == "norm":
        a = (0 - mean) / std
        b = (1 - mean) / std
        dist = truncnorm(a, b, loc=mean, scale=std)
        total = dist.rvs(size=num_samples)
    else:
        raise IOError(f"Unsupported distribution type {distribution}")

    return total, None
