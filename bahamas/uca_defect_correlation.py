# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import numpy as np
from scipy.stats import truncnorm, norm, uniform
import logging

from .utils import ODC_types, UCA_types, UCA_mean, UCA_sigma, read_excel

logger = logging.getLogger('BAHAMAS.UCA')


def get_uca_defect_correlation_dist(excel_file, distribution='norm', sheet_name='UCA Correlation'):
  """Assign distribution for each UCA defect correlation term

  Args:
      excel_file (str): Excel file to read in
      distribution (str, optional): Type of distribution (defaults to "norm")
      sheet_name (str, optional): Name of the sheet with UCA correlation data (defaults to "UCA Correlation")

  Returns:
      dict: UCA defect correlation distribution, {'UCA type':{'ODC type':Dist},...}
  """
  logger.info('Construct UCA ODC defect correlation distribution.')

  if distribution != 'norm':
    raise IOError(f'Unrecognized distribution {distribution}. Valid distribution is "norm"!')

  df = read_excel(excel_file, sheet_name=sheet_name, index_col=0)
  dist_dict = {}
  for i, uca_name in enumerate(UCA_types):
    dist_dict[uca_name] = {}
    for odc in ODC_types:
      mean = df.at[odc, UCA_mean[i]]
      sigma = df.at[odc, UCA_sigma[i]]
      if mean == 0. and sigma == 0.:
        dist = uniform(loc=0., scale=1E-14)
      else:
        a = (0 - mean) / sigma
        b = (1 - mean) / sigma
        dist = truncnorm(a, b, loc=mean, scale=sigma)
        # dist = norm(loc=mean, scale=sigma)
      dist_dict[uca_name][odc] = dist
  return dist_dict
