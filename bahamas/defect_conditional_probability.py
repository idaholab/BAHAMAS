# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import pandas as pd
import logging
import numpy as np

logger = logging.getLogger('BAHAMAS.DCP')

def stage_dcp_calculation(excel_file, sheet_name):
  """Defect conditional probability calculation for each SDLC stage

  Args:
      excel_file (str): The filename of the spreadsheet with the review number and trigger coverage
      sheet_name (str): The sheet name in the spreadsheet with the data (i.e., the SDLC stage name)

  Returns:
      dcp (float): defect conditional probability
  """
  logger.info('Calculate DCP for SDLC "%s" stage', sheet_name)
  # TODO: how to determine G value?
  # G = 0.25 # Based on normalization
  G = 1.0
#   G = 0.125 # given by previous implementation, need to be verified
  df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=["Review Number","Trigger Coverage"])
  df = df.dropna()
  if df.empty:
    logger.error('Try to process %s, but got empty inputs!', excel_file)
    raise IOError(f'Try to process {excel_file}, but got empty inputs!')
  reviews = df.iloc[:, 0].mean()
  triggers = df.iloc[:, 1].mean()
  dcp = G*np.exp(-4.*reviews*triggers)

  return dcp
