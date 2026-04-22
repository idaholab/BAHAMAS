"""
Created on September 7, 2025
@author: wangc, chene
"""
import pandas as pd
import warnings
import sys
import os
import copy
warnings.filterwarnings('ignore')

import logging

logger = logging.getLogger('BAHAMAS.CCCG')

########### internal functions

def check_valid(src_arr):
    """Check if group is empty

    Args:
        src_arr (list or pd.DataFrame): data to check

    Returns:
        bool: True if the group is not empty else False
    """
    if len(src_arr) == 0:
        return False

    return True

def clean_string(s):
    """remove "None" and "nan" from str that are separated by ";"

    Args:
        s (str): string to clean

    Returns:
        str: cleaned string
    """
    if pd.isna(s):
        return s
    return ';'.join([item for item in s.split(';') if item != 'None' and item != 'nan'])

def merge_multi_lists(*arg):
    """Merge multiple pd.DataFrame CCCG data and remove duplicates

    Args:
        arg (list): list of pd.DataFrame CCCG data

    Returns:
        list: Merged CCCG data without duplications
    """
    master = list()
    for pd_multi in arg:
        master.extend(pd_multi)
    master = drop_dup(master)
    return master

def drop_dup(list_pd):
    """Drop duplicated CCCG data

    Args:
        list_pd (list): list of pd.DataFrame (CCCG data)

    Returns:
        list: list of pd.DataFrame (CCCG data) without duplications
    """
    filtered_list_pd = list()

    flag = False

    for pd_tmp in list_pd:
        if len(filtered_list_pd) == 0:
            filtered_list_pd.append(list_pd[0])
            continue

        for c in filtered_list_pd:
            # Drop index comparison
            c = c.reset_index(drop=True)
            pd_tmp = pd_tmp.reset_index(drop=True)
            if pd_tmp.equals(c):
                flag = True
        if not flag:
            filtered_list_pd.append(pd_tmp)
        flag = False

    return filtered_list_pd

def unique_cells(src_arr):
    """Identify the unique inputs/designs/functions for given coupling factor (i.e., Input, Function and Design)

    Args:
        src_arr (pd.DataFrame): Expanded Coupling Factor data for single coupling factor

    Returns:
        list: list of unique inputs/designs/functions among all components
    """
    arr_cols = pd.concat([src_arr[col] for col in src_arr], ignore_index=True)
    arr_unique = arr_cols.unique()
    arr_unique = [cell for cell in arr_unique if pd.notna(cell)]

    return arr_unique

def match_CCCG_on(src_arr, col_name):
    """Get a list of CCCGs based on single coupling factor, which means the CCCGs are grouped because
    they have at least one shared variable of the given coupling factor

    Args:
        src_arr (pd.DataFrame): Component table with expanded coupling factors
        col_name (str): coupling factor, Function_, Input_ or Design_

    Returns:
        list: list of CCCGs based on single coupling factor, arranged in order *_1, *_2, *_3, etc. where * represent the coupling factor
    """
    CCCG_arr = list()

    # Get columns that start with the coupling factor name, i.e., Function_, Input_, and Design_
    arr_cols = [col for col in src_arr.columns if col.startswith(col_name)]

    # Get unique values for single coupling factor among all components
    tmp = unique_cells(src_arr[arr_cols])

    # Filter the DataFrame to find rows where any col_name column contains the search string
    for t in tmp:
        matching_rows = src_arr[arr_cols].apply(lambda row: row == t).any(axis=1)

        # Get the rows that match the search string
        result_df = src_arr[matching_rows]
        if len(result_df) == 0:
            continue

        # Result is a CCCG
        CCCG_arr.append(result_df)

    CCCG_arr = drop_dup(CCCG_arr)

    return CCCG_arr

def match_CCCG_list_on(list_pd, col_name):
    """Identify CCCGs that are also have "col_name" coupling factor (this function is used for two or more shared coupling factors)

    Args:
        list_pd (list): list of pd.DataFrame of CCCGs
        col_name (str): coupling factor, Function_, Input_ or Design_

    Returns:
        list: CCCGs with additional coupling factor ("col_name")
    """
    CCCG_arr = list()

    for pd_tmp in list_pd:
        tmp = match_CCCG_on(pd_tmp, col_name)
        CCCG_arr.extend(tmp)

    CCCG_arr = drop_dup(CCCG_arr)

    return CCCG_arr

def match_multi_on(src_arr, col_name):
    # Partially working, only matches on single dependency. Multiple dependencies matching is not implemented.
    CCCG_arr = list()

    # Get columns that start with the coupling factor name
    arr_cols = [col for col in src_arr.columns if col.startswith(col_name)]
    arr_rows = src_arr[arr_cols]

    # Filter the DataFrame to find rows where there are multiple dependencies
    for col_name in arr_cols:
        # Check if multiple dependencies
        matching_rows = src_arr[col_name].notna()

        tmp = src_arr[matching_rows].reset_index(drop=True)

        # Result is a CCCG
        for i in range(len(tmp)):
            row = tmp.loc[[i]]
            CCCG_arr.append(row)

    CCCG_arr = drop_dup(CCCG_arr)

    return CCCG_arr

def match_multi_list_on(list_pd, col_name):
    CCCG_arr = list()

    for pd_tmp in list_pd:
        tmp = match_multi_on(pd_tmp, col_name)

        for t in tmp:
            CCCG_arr.append(t)

    CCCG_arr = drop_dup(CCCG_arr)

    return CCCG_arr

class CCCG(object):
  """
  Compute CCCGs for given list of components of diversity and redundancy system

  Args:
      object (_type_): _description_
  """

  def __init__(self, file):
    self._sys_diagram = file
    self._cccg_final = []
    self._cccg_function = []
    self._cccg_input = []
    self._cccg_design = []
    self._cccg_single = []
    self._cccg_function_input = []
    self._cccg_function_design = []
    self._cccg_input_function = []
    self._cccg_input_design = []
    self._cccg_design_input = []
    self._cccg_design_function = []
    self._cccg_double = []
    self._cccg_function_input_design = []
    self._cccg_function_design_input = []
    self._cccg_input_design_function = []
    self._cccg_input_function_design = []
    self._cccg_design_input_function = []
    self._cccg_design_function_input = []
    self._cccg_triple = []
    self._function_all = []
    self._input_all = []
    self._design_all = []
    # self._output_file = "CCCGs.csv"

  def generate(self, config=None):
    """
    Generate CCCGs based on three coupling factors, i.e., Function, Input and Design
    """
    logger.info("Generating")
    # Read data file into Pandas
    df_pd = pd.read_csv(self._sys_diagram)

    # Expand Function_Config
    func_big = df_pd["Function_Config"].str.split('; ', expand=True)
    func_big.columns = [f'Function_{i+1}' for i in range(func_big.shape[1])]

    df_pd_tmp = pd.concat([df_pd.drop(columns=['Function_Config']), func_big], axis=1)

    # Expand Input_Config
    inpt_big = df_pd["Input_Config"].str.split('; ', expand=True)
    inpt_big.columns = [f'Input_{i+1}' for i in range(inpt_big.shape[1])]

    df_pd_tmp = pd.concat([df_pd_tmp.drop(columns=['Input_Config']), inpt_big], axis=1)

    # Expand Design Config
    dsgn_big = df_pd["Design_Config"].str.split('; ', expand=True)
    dsgn_big.columns = [f'Design_{i+1}' for i in range(dsgn_big.shape[1])]

    df_pd_tmp = pd.concat([df_pd_tmp.drop(columns=['Design_Config']), dsgn_big], axis=1)

    # Get CCCG on single coupling factor
    self._cccg_function = match_CCCG_on(df_pd_tmp, 'Function_') # list[first variable pd.DataFrame, second variable pd.DataFrame, ...]
    self._cccg_design   = match_CCCG_on(df_pd_tmp, 'Design_')
    self._cccg_input    = match_CCCG_on(df_pd_tmp, 'Input_')

    # Merge all CCCGs on single coupling factor and drop duplicates
    self._cccg_single   = merge_multi_lists(self._cccg_function,
                                    self._cccg_design,
                                    self._cccg_input
                                    )
    # remove single entry since there is no other component that has shared coupling factors
    self._cccg_single = [x for x in self._cccg_single if len(x) != 1]

    # Get CCCG on two coupling factor
    self._cccg_function_input  = match_CCCG_list_on(self._cccg_function, 'Input_')
    self._cccg_function_design = match_CCCG_list_on(self._cccg_function, 'Design_')

    self._cccg_input_function  = match_CCCG_list_on(self._cccg_input, 'Function_')
    self._cccg_input_design = match_CCCG_list_on(self._cccg_input, 'Design_')

    self._cccg_design_input  = match_CCCG_list_on(self._cccg_design, 'Input_')
    self._cccg_design_function = match_CCCG_list_on(self._cccg_design, 'Function_')

    # Merge all CCCGs on two coupling factor and drop duplicates
    self._cccg_double   = merge_multi_lists(self._cccg_function_design,
                                    self._cccg_function_input,
                                    self._cccg_design_input,
                                    self._cccg_design_function,
                                    self._cccg_input_design,
                                    self._cccg_input_function
                                    )
    # remove single entry since there is no other component that has shared coupling factors
    self._cccg_double = [x for x in self._cccg_double if len(x) != 1]

    # Get CCCG on three coupling factor
    self._cccg_function_input_design = match_CCCG_list_on(self._cccg_function_input, 'Design_')
    self._cccg_function_design_input = match_CCCG_list_on(self._cccg_function_design, 'Input_')

    self._cccg_input_design_function = match_CCCG_list_on(self._cccg_input_design, 'Function_')
    self._cccg_input_function_design = match_CCCG_list_on(self._cccg_input_function, 'Design_')

    self._cccg_design_input_function = match_CCCG_list_on(self._cccg_design_input, 'Function_')
    self._cccg_design_function_input = match_CCCG_list_on(self._cccg_design_function, 'Input_')

    # Merge all CCCGs on triple coupling factor and drop duplicates
    self._cccg_triple   = merge_multi_lists(self._cccg_function_input_design,
                                    self._cccg_function_design_input,
                                    self._cccg_input_design_function,
                                    self._cccg_input_function_design,
                                    self._cccg_design_input_function,
                                    self._cccg_design_function_input,
                                    )
    # remove single entry since there is no other component that has shared coupling factors
    self._cccg_triple = [x for x in self._cccg_triple if len(x) != 1]

    # Merge all CCCGs and drop duplicates
    self._cccg_final = merge_multi_lists(self._cccg_single,
                                self._cccg_double,
                                self._cccg_triple
    )

  def get(self, name):
    """Get CCCGs

    Args:
        name (str): name for CCCGs group

    Returns:
        list (list of Pandas.DataFrame): List of CCCGs
    """
    if name == 'final':
      return self.aggregate(self._cccg_final)
    elif name == 'single':
      return self.aggregate(self._cccg_single)
    elif name == 'double':
      return self.aggregate(self._cccg_double)
    elif name == 'triple':
      return self.aggregate(self._cccg_triple)
    else:
      raise IOError(f'Unrecognized name "{name}"!')

  def write(self, data, fname, style='csv'):
    """Dump data

    Args:
        data (list of pandas.DataFrame): output data to dump
        fname (str): file name to save the data
        style (str, optional): type of file. Defaults to 'csv'.
    """
    logger.info("Save CCCGs into %s", fname)
    with open(fname, 'w', newline='', encoding='utf-8') as f:
      for df in data:
          # Write each DataFrame to the file
          df.to_csv(f, index=False)
          f.write('\n')

  def aggregate(self, cccgs):
    """Aggregate expanded Function, Input, Design into Function_Config, Input_Config and Design_Config

    Args:
        cccgs (list): list of pd.DataFrame (i.e., CCCGs)

    Returns:
        list: list of aggregated CCCGs
    """
    cccg_list = copy.deepcopy(cccgs) # deepcopy is required, otherwise data manipulation
    cccg_transfer = []
    for pd_arr in cccg_list:
        coupling_factor = []
        function_columns = [col for col in pd_arr.columns if col.startswith('Function_')]
        if len(function_columns) > 0:
          pd_arr["Function_Config"] = pd_arr[function_columns].apply(lambda row: ';'.join(sorted(row.values.astype(str))), axis=1)
          pd_arr.drop(columns=function_columns, inplace=True)
          pd_arr["Function_Config"] = pd_arr["Function_Config"].apply(clean_string)
          if len(pd_arr["Function_Config"]) > 1 and pd_arr["Function_Config"].nunique() == 1 and pd_arr["Function_Config"].iloc[0] != '':
              coupling_factor.append('Function')

        input_columns = [col for col in pd_arr.columns if col.startswith('Input_')]
        if len(input_columns) > 0:
          pd_arr["Input_Config"] = pd_arr[input_columns].apply(lambda row: ';'.join(sorted(row.values.astype(str))), axis=1)
          pd_arr.drop(columns=input_columns, inplace=True)
          pd_arr["Input_Config"] = pd_arr["Input_Config"].apply(clean_string)
          if len(pd_arr["Input_Config"]) > 1 and pd_arr["Input_Config"].nunique() == 1 and pd_arr["Input_Config"].iloc[0] != '':
              coupling_factor.append('Input')

        design_columns = [col for col in pd_arr.columns if col.startswith('Design_')]
        if len(design_columns) > 0:
          pd_arr["Design_Config"] = pd_arr[design_columns].apply(lambda row: ';'.join(sorted(row.values.astype(str))), axis=1)
          pd_arr.drop(columns=design_columns, inplace=True)
          pd_arr["Design_Config"] = pd_arr["Design_Config"].apply(clean_string)
          if len(pd_arr["Design_Config"]) > 1 and pd_arr["Design_Config"].nunique() == 1 and pd_arr["Design_Config"].iloc[0] != '':
              coupling_factor.append('Design')
        if len(coupling_factor) > 0:
          pd_arr['Coupling_Factor'] = ";".join(coupling_factor)
        cccg_transfer.append(pd_arr)

    return cccg_transfer

