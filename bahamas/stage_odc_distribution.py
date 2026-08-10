# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

from scipy.stats import beta
import logging

from .utils import ODC_types, SDLC_stages, read_excel

logger = logging.getLogger('BAHAMAS.ODC')

def get_stage_odc_dist(excel_file, distribution='beta', sheet_name='ODC'):
  """Get the distribution of each ODC defect at the given SDLC stage
  P(Defect type|SDLC Stage) = dist_dict['SDLC Stage']['Defect type']

  Args:
      excel_file (str): Filename of the excel file to read in
      distribution (str, optional): Type of distribution to use (defaults to "beta")
      sheet_name (str, optional): Name of the sheet with the ODC data (defaults to "ODC")
  """
  logger.info('Construct ODC Conditional Distribution for each SDLC stage')
  alpha_prior = 0.5
  beta_prior = 0.5
  dist_dict = {}

  df = read_excel(excel_file, sheet_name=sheet_name)
  for _, row in df.iterrows():
    dist_dict[row.Stages] = {}
    total = row.Total
    for odc in ODC_types:
      val = getattr(row, odc)
      if distribution == 'beta':
        a = alpha_prior + val
        b = beta_prior + total - val
        dist  = beta(a, b)
      else:
        raise IOError(f"Unsupported distribution type {distribution} for function 'get_odc_dist'")
      dist_dict[row.Stages][odc] = dist
  return dist_dict




