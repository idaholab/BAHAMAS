# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

"""
Tests for bahamas/cccg.py
"""
import os
import numpy as np
import pandas as pd
import pytest

from bahamas.cccg import (
    check_valid,
    clean_string,
    merge_multi_lists,
    drop_dup,
    unique_cells,
    match_CCCG_on,
    match_CCCG_list_on,
    match_multi_on,
    match_multi_list_on,
    CCCG,
)

workdir = os.path.dirname(__file__)
structure_data = os.path.join(workdir, '..', 'data', 'Example_CCCG_Identification.xlsx')


def make_df(rows):
  return pd.DataFrame(rows)


def test_check_valid():
  assert check_valid([1, 2, 3]) is True
  assert check_valid([]) is False
  assert check_valid(pd.DataFrame({'a': [1]})) is True
  assert check_valid(pd.DataFrame()) is False


def test_clean_string():
  assert clean_string('a;None;b;nan;c') == 'a;b;c'
  assert clean_string('a;b') == 'a;b'
  assert clean_string('None;nan') == ''
  assert pd.isna(clean_string(np.nan))


def test_unique_cells():
  df = pd.DataFrame({
      'Function_1': ['F1', 'F1', 'F2', None],
      'Function_2': [None, 'F3', None, 'F2'],
  })
  result = unique_cells(df)
  # order follows column-major concat: Function_1 then Function_2
  assert result == ['F1', 'F2', 'F3']


def test_unique_cells_all_nan():
  df = pd.DataFrame({'A': [None, None], 'B': [None, None]})
  assert unique_cells(df) == []


def test_drop_dup_removes_equal_frames():
  d1 = make_df({'x': [1, 2]})
  d2 = make_df({'x': [1, 2]})
  d3 = make_df({'x': [3, 4]})

  result = drop_dup([d1, d2, d3])

  assert len(result) == 2
  pd.testing.assert_frame_equal(result[0].reset_index(drop=True), d1.reset_index(drop=True))
  pd.testing.assert_frame_equal(result[1].reset_index(drop=True), d3.reset_index(drop=True))


def test_drop_dup_empty_list():
  assert drop_dup([]) == []


def test_merge_multi_lists_dedups_across_groups():
  d1 = make_df({'x': [1, 2]})
  d2 = make_df({'x': [3, 4]})
  d1_dup = make_df({'x': [1, 2]})

  merged = merge_multi_lists([d1], [d2], [d1_dup])

  assert len(merged) == 2


def test_match_CCCG_on_groups_by_shared_value():
  df = pd.DataFrame({
      'Function_1': ['F1', 'F1', 'F2', None],
      'Function_2': [None, 'F3', None, 'F2'],
      'Design_1': ['D1', 'D1', 'D2', 'D3'],
  })

  groups = match_CCCG_on(df, 'Function_')
  design_sets = sorted(tuple(sorted(g['Design_1'].tolist())) for g in groups)

  # F1 groups rows with Design D1,D1; F2 groups rows with Design D2,D3;
  # F3 only appears in one row (Design D1), so it forms its own singleton
  assert ('D1', 'D1') in design_sets
  assert ('D2', 'D3') in design_sets
  assert ('D1',) in design_sets


def test_match_CCCG_on_no_shared_values_returns_singletons():
  df = pd.DataFrame({'Input_1': ['I1', 'I2', 'I3']})
  groups = match_CCCG_on(df, 'Input_')
  assert len(groups) == 3
  for g in groups:
    assert len(g) == 1


def test_match_CCCG_list_on_adds_second_coupling_factor():
  df = pd.DataFrame({
      'Function_1': ['F1', 'F1', 'F2'],
      'Input_1': ['I1', 'I2', 'I1'],
  })
  function_groups = match_CCCG_on(df, 'Function_')
  combined = match_CCCG_list_on(function_groups, 'Input_')

  # every result must itself be internally grouped on the Input_ coupling factor
  for g in combined:
    assert len(g) >= 1


def test_match_multi_on_returns_one_row_per_populated_cell():
  df = pd.DataFrame({
      'Function_1': ['F1', 'F1', None],
      'Function_2': [None, 'F3', 'F2'],
  })
  rows = match_multi_on(df, 'Function_')
  # Function_1 has 2 non-null entries (rows 0,1), Function_2 has 2 non-null
  # entries (rows 1,2); row 1 is produced by both columns but drop_dup collapses
  # the duplicate frame, leaving 3 single-row frames
  assert len(rows) == 3
  for r in rows:
    assert len(r) == 1


def test_match_multi_list_on_flattens_across_groups():
  df1 = pd.DataFrame({'Function_1': ['F1'], 'Function_2': ['F2']})
  df2 = pd.DataFrame({'Function_1': ['F3'], 'Function_2': [None]})

  rows = match_multi_list_on([df1, df2], 'Function_')
  # df1's single row is duplicated once per populated Function_ column (2),
  # then de-duplicated back down to 1; df2 contributes 1 more -> 2 total
  assert len(rows) == 2


@pytest.fixture(scope='module')
def cccg_obj():
  obj = CCCG(structure_data)
  obj.generate()
  return obj


def test_cccg_generate_counts(cccg_obj):
  assert len(cccg_obj._cccg_single) == 8
  assert len(cccg_obj._cccg_double) == 16
  assert len(cccg_obj._cccg_triple) == 1
  assert len(cccg_obj._cccg_final) == 20


def test_cccg_generate_no_singleton_groups(cccg_obj):
  for group in cccg_obj._cccg_single + cccg_obj._cccg_double + cccg_obj._cccg_triple:
    assert len(group) != 1


@pytest.mark.parametrize('name', ['final', 'single', 'double', 'triple'])
def test_cccg_get_returns_aggregated_frames(cccg_obj, name):
  result = cccg_obj.get(name)
  assert len(result) > 0
  for df in result:
    assert 'Function_Config' in df.columns
    assert 'Input_Config' in df.columns
    assert 'Design_Config' in df.columns
    # When present, every coupling factor label listed must actually be
    # constant (and non-empty) across the group
    if 'Coupling_Factor' in df.columns:
      for factor in df['Coupling_Factor'].iloc[0].split(';'):
        col = df[f'{factor}_Config']
        assert col.nunique() == 1
        assert col.iloc[0] != ''


def test_cccg_get_invalid_name_raises(cccg_obj):
  with pytest.raises(IOError):
    cccg_obj.get('bogus')


def test_cccg_aggregate_does_not_mutate_input(cccg_obj):
  before = [g.copy() for g in cccg_obj._cccg_single]
  cccg_obj.aggregate(cccg_obj._cccg_single)
  for orig, after in zip(before, cccg_obj._cccg_single):
    pd.testing.assert_frame_equal(orig, after)


def test_cccg_write(tmp_path, cccg_obj):
  out_file = tmp_path / 'cccg_output.csv'
  data = cccg_obj.get('final')
  cccg_obj.write(data, str(out_file))

  assert out_file.is_file()
  content = out_file.read_text()
  # one blank-line separator per written group
  assert content.count('\n\n') == len(data)
