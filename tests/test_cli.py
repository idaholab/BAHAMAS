# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

"""
Tests for BAHAMAS command line execution using the example TOML inputs.
"""
import os
import sys
import subprocess

import pytest

repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
examples_dir = os.path.join(repo_dir, 'examples')
bbn_toml = os.path.join(examples_dir, 'bbn.toml')
ccf_toml = os.path.join(examples_dir, 'ccf.toml')


def run_cli(args, cwd):
  """Run `python -m bahamas.main` with the given arguments

  Args:
      args (list): command line arguments to pass after the module name
      cwd (str): working directory to run the command in

  Returns:
      subprocess.CompletedProcess: result of the command execution
  """
  cmd = [sys.executable, '-m', 'bahamas.main'] + args
  return subprocess.run(
      cmd, cwd=cwd, capture_output=True, text=True, timeout=120
  )


def test_cli_help():
  result = run_cli(['--help'], cwd=repo_dir)
  assert result.returncode == 0
  assert '--input' in result.stdout
  assert '--output' in result.stdout


def test_cli_missing_input_file(tmp_path):
  result = run_cli(
      ['-i', os.path.join(examples_dir, 'does_not_exist.toml'), '-o', 'out.csv'],
      cwd=tmp_path,
  )
  assert result.returncode != 0
  assert 'FileNotFoundError' in result.stderr


def test_cli_bbn(tmp_path):
  result = run_cli(['-i', bbn_toml, '-o', 'output.csv'], cwd=tmp_path)

  assert result.returncode == 0, result.stderr
  assert 'Welcome to use BAHAMAS!' in result.stderr
  assert 'TOML input file is valid.' in result.stderr
  assert 'Start BBN Calculation' in result.stderr
  assert 'Software total failure:' in result.stderr
  assert 'End BBN Calculation' in result.stderr
  assert '... Complete!' in result.stderr

  for uca in ['UCA-A', 'UCA-B', 'UCA-C', 'UCA-D']:
    assert f'UCA type: {uca}' in result.stderr

  assert os.path.isfile(os.path.join(tmp_path, 'bahamas.log'))


def test_cli_ccf(tmp_path):
  result = run_cli(['-i', ccf_toml, '-o', 'output.csv'], cwd=tmp_path)

  assert result.returncode == 0, result.stderr
  assert 'Welcome to use BAHAMAS!' in result.stderr
  assert 'TOML input file is valid.' in result.stderr
  assert 'Start CCCGs generation' in result.stderr
  assert 'End CCCGs generation' in result.stderr
  assert '... Complete!' in result.stderr

  assert os.path.isfile(os.path.join(tmp_path, 'bahamas.log'))
