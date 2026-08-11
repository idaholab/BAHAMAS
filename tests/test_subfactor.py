# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

"""
Tests for bahamas/subfactor.py
"""
import pytest

from bahamas.subfactor import (
    compute_beta,
    compute_phi,
    subfactor_score_software,
    defense_factor,
)


def test_compute_beta_known_values():
  scores = {
      'Redundancy': 'A',
      'Input Similarity': 'B',
      'Understanding': 'C',
      'Analysis and Feedback': 'D',
      'Human-Machine Interface': 'E',
      'Safety Culture and Training': 'A',
      'Access Control': 'B',
      'Tests': 'C',
  }
  beta, ind = compute_beta(scores)

  denom = subfactor_score_software['Denominator']
  expected_ind = {factor: subfactor_score_software[factor][score] / denom
                  for factor, score in scores.items()}
  expected_beta = sum(expected_ind.values())

  assert beta == pytest.approx(expected_beta)
  for factor, value in expected_ind.items():
    assert ind[factor] == pytest.approx(value)


def test_compute_beta_a_plus_falls_back_to_a():
  # "Understanding" has no explicit A+ score, so A+ should reuse the A value
  beta_a, ind_a = compute_beta({'Understanding': 'A'})
  beta_a_plus, ind_a_plus = compute_beta({'Understanding': 'A+'})

  assert beta_a_plus == pytest.approx(beta_a)
  assert ind_a_plus['Understanding'] == pytest.approx(ind_a['Understanding'])


def test_compute_beta_b_plus_falls_back_to_b():
  # "Input Similarity" has no explicit B+ score, so B+ should reuse the B value
  beta_b, ind_b = compute_beta({'Input Similarity': 'B'})
  beta_b_plus, ind_b_plus = compute_beta({'Input Similarity': 'B+'})

  assert beta_b_plus == pytest.approx(beta_b)
  assert ind_b_plus['Input Similarity'] == pytest.approx(ind_b['Input Similarity'])


def test_compute_beta_unknown_subfactor_raises():
  with pytest.raises(IOError):
    compute_beta({'Nonexistent Factor': 'A'})


def test_compute_beta_unknown_score_raises():
  with pytest.raises((IOError, KeyError)):
    compute_beta({'Redundancy': 'Z'})


def test_compute_phi_known_values():
  scores = {
      'Input Similarity': 'A',
      'Understanding': 'B',
      'Analysis': 'C',
      'MMI': 'D',
      'Safety Culture': 'E',
      'Control': 'A',
      'Tests': 'B',
  }
  phi, ind = compute_phi(scores)

  denom = defense_factor['Denominator']
  expected_ind = {factor: defense_factor[factor][score] / denom
                  for factor, score in scores.items()}
  expected_phi = sum(expected_ind.values())

  assert phi == pytest.approx(expected_phi)
  for factor, value in expected_ind.items():
    assert ind[factor] == pytest.approx(value)


def test_compute_phi_a_plus_falls_back_to_a():
  phi_a, ind_a = compute_phi({'Understanding': 'A'})
  phi_a_plus, ind_a_plus = compute_phi({'Understanding': 'A+'})

  assert phi_a_plus == pytest.approx(phi_a)
  assert ind_a_plus['Understanding'] == pytest.approx(ind_a['Understanding'])


def test_compute_phi_unknown_subfactor_raises():
  with pytest.raises(IOError):
    compute_phi({'Nonexistent Factor': 'A'})


def test_compute_phi_b_plus_not_supported_raises():
  # defense_factor has no B+ entries and compute_phi has no B+ fallback
  with pytest.raises((IOError, KeyError)):
    compute_phi({'Input Similarity': 'B+'})
