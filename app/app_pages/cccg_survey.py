# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
from .regression import get_sil_val
from scipy.stats import loguniform
import numpy as np
import os, sys
from collections import OrderedDict

# Bahamas Module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from bahamas.subfactor import compute_beta, compute_phi

input_sim_scale = ['Not at all', 'To a small extent', 'To a moderate extent', 'To a great extent', 'Fully and systematically']
input_sim_scale_value = [1., 0.75, 0.5, 0.25, 0.]
input_sim_response_dict = dict(zip(input_sim_scale, input_sim_scale_value))

score_transform = {4:'A', 3:'B', 2:'C', 1:'D', 0:'E', 'A':4, 'B':3, 'C':2, 'D':1, 'E':0}

subfactors = ["Input Similarity", "Understanding", "Analysis and Feedback", "Human-Machine Interface", "Safety Culture and Training", "Access Control", "Tests"]

input_sim_qa = {'##### What of Information: What is the information or variable of interest (pressure, temperature, etc.) and is that shared by the members of the CCCG?': 'Considering the elements of the CCCG, to what extent do the elements rely on the same “What” information?',
                '##### Where of Information: Where does the information come from (pressure sensor, human messenger, external system, etc.)  and is that shared by the members of the CCCG? ':'Considering the elements of the CCCG, to what extent do the elements rely on the same “where” information?',
                '##### Format of Information: What is the format of the information or data and is that the same format employed for all members of the CCCG? ': "Considering the elements of the CCCG, to what extent do the elements rely on the same “format” information?",
                '##### Means of Information: How is the information transferred (wireless, fiberoptic, wired, etc.) and is that the same means employed for all members of the CCCG?': 'Considering the elements of the CCCG, to what extent do the elements rely on the same “how” information?',
                '##### When of Information: When is the information required (i.e. timing of information) and is that the same timing employed for all members of the CCCG?': 'Considering the elements of the CCCG, to what extent do the elements rely on the same “when” information?'}

understanding_qa = {'Novelty: Considering the elements of the CCCG, to what extent do the elements rely on the novel, principles, configurations, or  information?':
  ['Not Novel: The CCCG elements contain well-understood concepts, reused technology, or similar configurations to previously implemented systems.',
  'Novel: The CCCG can be described as first-of-a-kind, software with limited operational experience, or contains concepts that are not fully understood.'],
  'Complexity: Do the members of the CCCG perform only a single dedicated function/action?':
  ['Yes', 'No'],
  'Misfit: Do the members of the CCCG ?':
  ["""High Misfit: The system has high "misfit" if the if the majority of the system's functionality is accomplished through off-the-shelf systems, pre-existing functions, or established functions.""",
  """Low Misfit: The system has low “misfit” if there are zero to minimal off-the-shelf systems, pre-existing functions, or established functions. (mostly purpose-built functions)."""],
  'Experience: Indicate the operational experience of the CCCG':
  ['More: Operational experience is more than 10 years.', 'Less: Operational experience is less than 10 years.']
  }

understanding_score = {'Novel':1, 'Not Novel': 0,
                      'Yes': 0, 'No': 1,
                      'High Misfit': 0, 'Low Misfit': 1,
                      'More': 0, 'Less': 1}
afa_qa = OrderedDict()
afa_qa['Analysis: Indicate the level of risk analysis that was performed for the CCCG'] = ['No-An: The CCCG has not been identified and no CCF analysis has been carried out for the specific CCCG.',
  'An: The CCCG is identified as a potential hazard. Little consideration is made to how a CCF within a CCCG might influence the system.',
  'An+: The CCCG is identified and analyzed for its threat to system performance. CCF is considered. Hazard and consequences are tracked as part of an FTA or other formal PRA tools.']
afa_qa['Feedback: Indicate the level of feedback that was performed for the CCCG'] = ['No-F: No feedback concerning the CCCG was provided to the design team.',
  'F: Feedback was provided to the design team concerning the specific CCCG.',
  'F+: Detailed feedback was provided to the design team. There is evidence that feedback led to actionable recommendations that are document trackable']
afa_qa['Awareness: Indicate the level of awareness of CCF as evident in the design with respect to the CCCG.'] = ['Level 1: There is no evidence of awareness for CCF of the CCCG. No dedicated attempt to prevent software CCF was included in the design (i.e., duplication of software in redundant trains). The CCCG has low levels or no built-in redundancy.',
  'Level 2: There is evidence of general CCF knowledge as demonstrated by the existence of redundant configurations within the design. No diversity is used to support design.',
  'Level 3: There is evidence of awareness of software-based CCFs. Diverse software configurations are used. The analyst may also reason that there are other advanced methods beyond diversity that merit a score beyond Level 2.']

key = [['No-An', 'No-F', 'Level 1'], ['No-An', 'No-F', 'Level 2'], ['No-An', 'No-F', 'Level 3'],
      ['An', 'F', 'Level 1'], ['An', 'F', 'Level 2'], ['An', 'F', 'Level 3'],
      ['An+', 'F', 'Level 1'], ['An+', 'F', 'Level 2'], ['An+', 'F', 'Level 3'],
      ['An', 'F+', 'Level 1'], ['An', 'F+', 'Level 2'], ['An', 'F+', 'Level 3'],
      ['An+', 'F+', 'Level 1'], ['An+', 'F+', 'Level 2'], ['An+', 'F+', 'Level 3']
    ]
val = ['A', 'B', 'C',
      'B', 'C', 'D',
      'B', 'C', 'D',
      'B', 'C', 'D',
      'B', 'D', 'E']

afa_score = {}
for k, v in zip(key, val):
  name = '|'.join(k)
  afa_score[name] = v

hmi_qa = OrderedDict()
hmi_qa['Interaction Frequency: Indicate the level of interaction the user/operator/staff has with the CCCG'] = ['Minimal: Interactions are low or infrequent.',
                                                                                                                'Normal: Interactions are regular, normal, scheduled, or routine.']
hmi_qa['Operator/User: Indicate how user/operator interactions are controlled for the CCCG'] = ['No Procedures: There are no written procedures or guidance to interact with the CCCG.',
                                                                                                'Procedures: There are written procedures to control the operation.',
                                                                                                'Checklists: Checklists to compliment procedures.']
hmi_qa['Maintenance: Indicate how maintenance activities are controlled for the CCCG.'] = ['A: No guidance or controls.', 'B: Work checked by a supervisor.',
                                                                                          'C: Post maintenance testing.', 'D: Work checked and tested.',
                                                                                          'E: All maintenance activities have specific acceptance tests.']

operator_score = {'Normal|No Procedures':4, 'Minimal|No Procedures':3, 'Normal|Procedures':3,  'Minimal|Procedures':2,
      'Normal|Checklists':1, 'Minimal|Checklists':0}
maintenance_score = {'A':4, 'B':3, 'C':2, 'D':1, 'E':0}

culture_qa = OrderedDict()
culture_qa['Training: What level of education has the staff received regarding the components and software of the CCCG?'] = ['On-the-job: No formalized education concerning any aspect of the CCCG.',
                                                                                                                            'General: Basic general education concerning the CCCG.',
                                                                                                                            'Specialized: Detailed training, and education related to the specific components and software of the CCCG. May include simulator training, when applicable. Also, years of experience may be considered.']
culture_qa['Safety Culture: What level of education has the staff received regarding the components and software of the CCCG?'] = ['Casual: Staff may or may not have safety in mind. No safety training.',
                                                                                                                                'Safety Oriented: Staff have safety in mind. Periodic safety training related to working with the components/software of the CCCG.',
                                                                                                                                'Safety Oriented+: Staff have safety in mind, there is a clearly defined organizational safety culture, safety policies, regular safety training.']
culture_score = {'Casual': 4, 'Safety Oriented':2, 'Safety Oriented+': 0, 'On-the-job': 4, 'General':2, 'Specialized':0}


control_qa = {'What level of access control is in place for the components and software of the CCCG?':
  ['A: No control, open access networks, unsecured physical locations.',
  'B: Secured physical locations, private networks, general institutional access, multiple unrelated software systems found in single physical location.',
  'C: Secured physical locations, private networks, limited institutional access (e.g., authorized personnel only, and passwords).',
  'D: Secured physical locations, private networks, limited access to authorized and trained personnel only. Close supervision is employed. The area where software is found is limited to software of similar purposes (i.e., multiple software programs on the same machine but all related to similar purpose) multiple systems may be present in the same area.',
  'E: Secured physical locations, private networks, extremely limited access, trained personnel only operating under close supervision, specialized machines (i.e., no other software present), only a single-purpose system is present in the area.']
  }

testing_qa = {'What level of testing is planned or has been implemented for the CCCG?':
  ['A: No testing of the system, specifically the CCCG.',
  'B: Individual unit testing (single examples for each software type within CCCG). An example unit has been tested.',
  'C: Detailed testing is performed on an example system (i.e., CCCG). Testing includes verification and compliance testing to ensure the CCCG meets all required criteria as a unit.',
  'D: Commissioning tests performed on the specific CCCG to be employed. Detailed integration testing of the CCCG, in addition to stress testing.',
  'E: In addition to C&D levels, a long-term test is conducted for the CCCG. The test is performed in parallel with existing system for approximately for a specified duration (e.g.,1 year.)']
  }



def app():

  st.write(afa_score['An|F|Level 2'])

  st.title("Software Common Cause Failure Survey")
  qa_default_index = 3
  survey_data = {}
  # Information or Input Similarity

  st.header('Information or Input Similarity:')
  ind = 0
  weight = 0.0
  score = None
  for key, val in input_sim_qa.items():
    ind += 1
    st.markdown(key)
    response = st.radio(val, input_sim_scale, horizontal=True, key='input_sim' + str(ind), index=qa_default_index)
    weight += input_sim_response_dict[response]

  ave = weight/ind
  # ToDo: need to align with CCF paper
  if ave == 0.:
    score = "E"
  elif ave <= 0.25:
    score = "D"
  elif ave <= 0.5:
    score = "C"
  elif ave <= 0.75:
    score = "B"
  else:
    score = "A"
  survey_data["Input Similarity"] = score

  headers = ['Understanding', 'Analysis and Feedback', 'Human-Machine Interface', 'Safety Culture and Training', 'Access Control', 'Tests']
  qa = [understanding_qa, afa_qa, hmi_qa, culture_qa, control_qa, testing_qa]
  for h, q in zip(headers, qa):
    st.header(h)
    ind = 0
    score = None
    response = []
    for key, val in q.items():
      ind += 1
      if ':' in key:
        m, k = key.split(':')
        st.markdown(f'##### {m.strip()}')
      else:
        k = key
      captions = []
      options = []
      for v in val:
        if ':' in v:
          o, c = v.split(':')
          options.append(o.strip())
          captions.append(c.strip())
      if len(options) == 0:
        options = val
      if len(captions) == 0:
        captions = None

      r = st.radio(k, options, captions=captions, horizontal=False, key=h + str(ind), index=1)
      response.append(r)


    if h == 'Understanding':
      Ut = np.sum([understanding_score[k] for k in response])
      score = score_transform[Ut]
    elif h == 'Analysis and Feedback':
      name = '|'.join(response)
      score = afa_score[name]
    elif h == 'Human-Machine Interface':
      op = '|'.join(response[0:2])
      mt = response[2]
      s1 = operator_score[op]
      s2 = maintenance_score[mt]
      smax = max(s1, s2)
      score = score_transform[smax]
    elif h == 'Safety Culture and Training':
      cul = culture_score[response[0]]
      ed = culture_score[response[1]]
      m = max (cul, ed)
      score = score_transform[m]
    else:
      score = response[0]
    survey_data[h] = score

  with st.form("my_form"):
    st.info("**Assessment! Start here ↓**", icon="👋🏾")
    # with st.expander(":orange[**Refine Calculation**]"):
    # Advanced Settings (for the curious minds!)

    software_total_failure = st.number_input('Software Total Failure Probability', value=1.0e-4, format='%.2e', key="sfp")

    # The Big Red "Submit" Button!
    submitted = st.form_submit_button(
        "Evaluate", type="primary", use_container_width=True)


    # process data
    if submitted:
      st.write("Subfactor Scores:")
      st.write(survey_data)
      # compute defense factor
      beta = compute_beta(survey_data)
      st.write('Defense Factor:', beta)
      st.write('CCCG Failure Probability:', beta * software_total_failure)

    else:
        pass





