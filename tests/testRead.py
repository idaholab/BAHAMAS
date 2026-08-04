# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 09:45:55 2026

@author: CHENE
"""
import pandas as pd

# Subfactor
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


# Section Titles
score_transform = {4:'A', 3:'B', 2:'C', 1:'D', 0:'E', 'A':4, 'B':3, 'C':2, 'D':1, 'E':0}

input_sim_scale = ['Not at all', 'To a small extent', 'To a moderate extent', 'To a great extent', 'Fully and systematically']
input_sim_scale_value = [1., 0.75, 0.5, 0.25, 0.]
input_sim_response_dict = dict(zip(input_sim_scale, input_sim_scale_value))


understanding_score = {'Novel': 1, 'Not Novel': 0,
                       'Yes': 0, 'No': 1,
                       'High Misfit': 0, 'Low Misfit': 1,
                       'More': 0, 'Less': 1}

key = [
    ['No-An', 'No-F', 'Level 1'], ['No-An', 'No-F', 'Level 2'], ['No-An', 'No-F', 'Level 3'],
    ['An',    'No-F', 'Level 1'], ['An',    'No-F', 'Level 2'], ['An',    'No-F', 'Level 3'],
    ['An+',   'No-F', 'Level 1'], ['An+',   'No-F', 'Level 2'], ['An+',   'No-F', 'Level 3'],
    ['No-An', 'F',    'Level 1'], ['No-An', 'F', 'Level 2'], ['No-An', 'F',    'Level 3'],
    ['An',    'F',    'Level 1'], ['An',    'F', 'Level 2'], ['An',    'F',    'Level 3'],
    ['An+',   'F',    'Level 1'], ['An+',   'F', 'Level 2'], ['An+',   'F',    'Level 3'],
    ['No-An', 'F+',   'Level 1'], ['No-An', 'F+','Level 2'], ['No-An', 'F+',   'Level 3'],
    ['An',    'F+',   'Level 1'], ['An',    'F+','Level 2'], ['An',    'F+',   'Level 3'],
    ['An+',   'F+',   'Level 1'], ['An+',   'F+','Level 2'], ['An+',   'F+',   'Level 3']
]
# Key-Val Note: [No-An,F, *] and [No-An, F+, *] do not have key values as there cannot be feedback without analysis.

val = ['A', 'B', 'C',
       'A', 'B', 'C',
       'A', 'B', 'C',
       None, None, None,
       'B', 'C', 'D',
       'B', 'C', 'D',
       None, None, None,
       'B', 'C', 'D',
       'B', 'D', 'E']

afa_score = {}
for k, v in zip(key, val):
    name = '|'.join(k)
    afa_score[name] = v

# Human Machine Interface
hmi_operator_score = {'Normal|No Procedures': 4, 'Minimal|No Procedures': 3, 'Normal|Procedures': 3,  'Minimal|Procedures': 2, 'Normal|Checklists': 1, 'Minimal|Checklists': 0}
hmi_maintenance_score = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}
culture_score = {'Casual': 4, 'Safety Oriented': 2, 'Safety Oriented+': 0, 'On-the-job': 4, 'General': 2, 'Specialized': 0}
score_transform = {4:'A', 3:'B', 2:'C', 1:'D', 0:'E', 'A':4, 'B':3, 'C':2, 'D':1, 'E':0}

# concatenate all scoring tables into a single table
result = {}
for d in [culture_score, hmi_maintenance_score, hmi_operator_score, afa_score, understanding_score, input_sim_response_dict]:
    for key, value in d.items():
        if key not in result:
            result[key] = value

data = pd.read_excel("./Template_CCCG_Survey.xlsx", usecols=[1], sheet_name="Questions", engine="openpyxl")

# Concatenate multiple entry rows together to match key-value format

# Concatenate rows 8, 9, and 10 → "An|F|Level 2"
combined_8_10 = data.iloc[9:12]
values8910 = combined_8_10.astype(str).values.flatten()
result8910 = "|".join(values8910)

# Concatenate rows 11 and 12 → "Normal|Procedures"
combined_11_12 = data.iloc[12:14]
values1112 = combined_11_12.astype(str).values.flatten()
result1112 = "|".join(values1112)

# Build the new dataframe
new_values = []

# Rows 0–7 unchanged
new_values.extend(data.iloc[0:9]["Answers"].tolist())

# Insert concatenated rows 8–10
new_values.append(result8910)

# Insert concatenated rows 11–12
new_values.append(result1112)

# Rows 13–18 unchanged (skipping original rows 8–12)
new_values.extend(data.iloc[14:]["Answers"].tolist())

# Calculate new score values based on new scoring list.
survey_data = {}

# For Input Similarity
weight = 0
weight += result[new_values[0]]
weight += result[new_values[1]]
weight += result[new_values[2]]
weight += result[new_values[3]]
weight += result[new_values[4]]
ave     = weight/5
if ave == 1:
    score = "E"
elif ave >= 0.75:
    score = "D"
elif ave >= 0.5:
    score = "C"
elif ave >= 0.25:
    score = "B"
else:
    score = "A"
survey_data["Input Similarity"] = score

# For Understanding
Ut = result[new_values[5]] + result[new_values[6]] + result[new_values[7]] + result[new_values[8]]
survey_data["Understanding"] = score_transform[Ut]

# For Analysis and Feedback
score = result[new_values[9]]
survey_data["Analysis and Feedback"] = score

# For Human-Machine Interface
m  = max(result[new_values[10]], result[new_values[11]])
survey_data["Human-Machine Interface"] = score_transform[m]

# For Safety Culture and Training
m = max(result[new_values[12]], result[new_values[13]])
score = score_transform[m]
survey_data["Safety Culture and Training"] = score

# For Access Control 
survey_data["Access Control"] = new_values[14]

# For Tests
survey_data["Tests"] = new_values[15]

# Compute scoring data
t = compute_beta(survey_data)
print(t)