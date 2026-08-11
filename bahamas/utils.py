# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import logging
import pathlib
import toml
import os
import pandas as pd

logger = logging.getLogger()

# software development lifecycle stages
SDLC_stages = ['Concept', 'Requirement', 'Design', 'Implementation', 'Testing', 'Install and Maintenance']

# Define action type names
human_error_modes = ['D1', 'D2', 'C', 'OC', 'D1C', 'D1OC', 'D2C', 'D2OC', 'O', 'D1O', 'D2O']

# ODC types
ODC_types = ['Algorithm', 'Assignment', 'Checking', 'Documentation', 'Function', 'Interface', 'Relationship', 'Timing']

UCA_types = ['UCA-A', 'UCA-B', 'UCA-C', 'UCA-D']

UCA_mean = ['UCA-A Mean',	'UCA-B Mean',	'UCA-C Mean',	'UCA-D Mean']

UCA_sigma = ['UCA-A Sigma',	'UCA-B Sigma','UCA-C Sigma','UCA-D Sigma']


def read_excel(*args, **kwargs):
  """Read an excel file into a pandas DataFrame, stripping trailing/leading
  whitespace from string values (including the column index if it holds strings)

  Args:
      *args, **kwargs: Arguments passed directly to pandas.read_excel

  Returns:
      pandas.DataFrame: The parsed excel data with string values stripped
  """
  df = pd.read_excel(*args, **kwargs)
  for col in df.columns:
    if df[col].dtype == object:
      df[col] = df[col].apply(lambda val: val.strip() if isinstance(val, str) else val)
  if df.index.dtype == object:
    df.index = df.index.map(lambda val: val.strip() if isinstance(val, str) else val)
  return df


def read_toml(file_path):
  """Read TOML-formatted file

  Args:
      file_path (str): Path to the file

  Returns:
      dict: Dictionary of file content
  """
  with open(file_path, 'r') as file:
    path = pathlib.Path(file_path).parent
    data = toml.load(file)
    if 'BBN' in data:
      for f in data['BBN']['files']:
        data['BBN']['files'][f] = os.path.join(path, data['BBN']['files'][f])
    if 'CCF' in data:
      for f in data['CCF']['files']:
        data['CCF']['files'][f] = os.path.join(path, data['CCF']['files'][f])
  return data
