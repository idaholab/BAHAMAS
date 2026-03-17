
# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

subfactor_score_software = {
  "Redundancy": {
    "A": 23976,
    "A+": 10112,
    "B": 4265,
    "B+": 1799,
    "C": 759,
    "D": 135,
    "E": 24
  },
  "Input Similarity": {
    "A": 23976,
    "A+": 10112,
    "B": 4265,
    "B+": None,
    "C": 759,
    "D": 135,
    "E": 24
  },
  "Understanding": {
    "A": 7992,
    "A+": None,
    "B": 1422,
    "B+": None,
    "C": 253,
    "D": 45,
    "E": 8
  },
  "Analysis and Feedback": {
    "A": 7992,
    "A+": None,
    "B": 1422,
    "B+": None,
    "C": 253,
    "D": 45,
    "E": 8
  },
  "Human-Machine Interface": {
    "A": 11988,
    "A+": None,
    "B": 2132,
    "B+": None,
    "C": 379,
    "D": 67,
    "E": 12
  },
  "Safety Culture and Training": {
    "A": 6993,
    "A+": None,
    "B": 1244,
    "B+": None,
    "C": 221,
    "D": 39,
    "E": 7
  },
  "Access Control": {
    "A": 4995,
    "A+": None,
    "B": 888,
    "B+": None,
    "C": 158,
    "D": 28,
    "E": 5
  },
  "Tests": {
    "A": 11988,
    "A+": None,
    "B": 2132,
    "B+": None,
    "C": 379,
    "D": 67,
    "E": 12
  },
  "Denominator": 100000.0
}

defense_factor = {
  "Input Similarity": {
    "A": 23976,
    "A+": 10112,
    "B": 4265,
    "C": 759,
    "D": 135,
    "E": 24
  },
  "Understanding": {
    "A": 7992,
    "A+": None,
    "B": 1422,
    "C": 253,
    "D": 45,
    "E": 8
  },
  "Analysis": {
    "A": 7992,
    "A+": None,
    "B": 1442,
    "C": 253,
    "D": 45,
    "E": 8
  },
  "MMI": {
    "A": 11988,
    "A+": None,
    "B": 2132,
    "C": 379,
    "D": 67,
    "E": 12
  },
  "Safety Culture": {
    "A": 6993,
    "A+": None,
    "B": 1244,
    "C": 221,
    "D": 39,
    "E": 7
  },
  "Control": {
    "A": 4995,
    "A+": None,
    "B": 888,
    "C": 158,
    "D": 28,
    "E": 5
  },
  "Tests": {
    "A": 11988,
    "A+": None,
    "B": 2132,
    "C": 379,
    "D": 67,
    "E": 12
  },
  "Denominator": 76000.0
}

def compute_beta(subfactor_dict):
  """Compute beta factor for CCF

  Args:
      subfactor_dict (dict): Dictionary of subfactors and their scores {"subfactor":"score"}

  Raises:
      IOError: Error if the score value can not be found

  Returns:
      float: beta factor value
  """
  tot = 0
  ind = {}
  for factor, score in subfactor_dict.items():
    if factor not in subfactor_score_software:
      raise IOError(f"Unidentified subfactor '{factor}'!")
    value = subfactor_score_software[factor][score]
    if value is None:
      if score == 'A+':
        value = subfactor_score_software[factor]['A']
      elif score == 'B+':
        value = subfactor_score_software[factor]['B']
      else:
        raise IOError(f'Unidentified value for subfactor "{factor}" with score "{score}" for beta factor calculation!')
    tot += value
    ind[factor] = value/subfactor_score_software['Denominator']
  beta = tot/subfactor_score_software['Denominator']
  return beta, ind

def compute_phi(subfactor_dict):
  """Compute defense factor for CCF

  Args:
      subfactor_dict (dict): Dictionary of subfactors and their scores {"subfactor":"score"}

  Raises:
      IOError: Error if the score value cannot be found

  Returns:
      float: defense factor value
  """
  tot = 0
  ind = {}
  for factor, score in subfactor_dict.items():
    if factor not in defense_factor:
      raise IOError(f"Unidentified subfactor '{factor}'!")
    value = defense_factor[factor][score]
    if value is None:
      if score == 'A+':
        value = defense_factor[factor]['A']
      else:
        raise IOError(f'Unidentified value for subfactor "{factor}" with score "{score}" for defense factor calculation!')
    tot += value
    ind[factor] = value/defense_factor['Denominator']
  phi = tot/defense_factor['Denominator']
  return phi, ind
