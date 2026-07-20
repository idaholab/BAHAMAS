# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

# built-in libraries
from bahamas.subfactor import compute_beta, compute_phi
import pandas as pd
from collections import OrderedDict
import numpy as np
from scipy.stats import loguniform
import streamlit as st
from io import BytesIO
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# implicit libraries

# explicit libraries

# %% --- Page Overview Text Descriptions ---
general_instructions = """
    There are two methods to input the data for the common cause evaluation survey. Option 1, manually inputing the data using the provided web interface. Option 2, uploading an Excel file covering the same questions. 
"""

# --- End Page Overview

# %% --- Download Template Text ---
questions = [
    "What is the information or variable of interest (pressure, temperature, etc.) and is that shared by the members of the CCCG?",
    "Where does the information come from (pressure sensor, human messenger, external system, etc.) and is that shared by the members of the CCCG?",
    "What is the format of the information or data and is that the same format employed for all members of the CCCG?",
    "How is the information transferred (wireless, fiberoptic, wired, etc.) and is that the same means employed for all members of the CCCG?",
    "When is the information required (i.e. timing of information) and is that the same timing employed for all members of the CCCG?",
    "Considering the elements of the CCCG, to what extent do the elements rely on the novel, principles, configurations, or information? (Not Novel/Novel)",
    "Do the members of the CCCG perform only a single dedicated function/action? (Y/N)",
    "Do the members of the CCCG? (High/Low Misfit)",
    "Indicate the operational experience of the CCCG (More/Less)",
    "Indicate the level of risk analysis that was performed for the CCCG (No-An/An/An+)",
    "Indicate the level of feedback that was performed for the CCCG (No-F/F/F+)",
    "Indicate the level of awareness of CCF as evident in the design with respect to the CCCG (Level 1/2/3)",
    "Indicate the level of interaction the user/operator/staff has with the CCCG (Minimal/Normal)",
    "Indicate how user/operator interactions are controlled for the CCCG (No Procedures/Procedures/Checklists)",
    "Indicate how maintenance activities are controlled for the CCCG (A/B/C/D/E)",
    "What level of education has the staff received regarding the components and software of the CCCG? (On-the-job/General/Specialized)",
    "What level of education has the staff received regarding the components and software of the CCCG? (Casual/Safety-Oriented/Safety Oriented+)",
    "What level of access control is in place for the components and software of the CCCG?",
    "What level of testing is planned or has been implemented for the CCCG?"
]
answers = [""] * len(questions)
dropdown_values = [
    "Not at all",
    "To a small extent",
    "To a moderate extent",
    "To a great extent",
    "Fully and systematically",
    "Not Novel",
    "Novel",
    "Yes",
    "No",
    "High Misfit",
    "Low Misfit",
    "More",
    "Less",
    "No-An",
    "An",
    "An+",
    "No-F",
    "F",
    "F+",
    "Level 1",
    "Level 2",
    "Level 3",
    "Minimal",
    "Normal",
    "No Procedures",
    "Procedures",
    "Checklists",
    "A",
    "B",
    "C",
    "D",
    "E",
    "On-the-job",
    "General",
    "Specialized",
    "Casual",
    "Safety Oriented",
    "Safety Oriented+"
]
manual_instructions = """
            For manual input, navigate and complete the survey across the below tabs:
            <ol>
                <li> <strong>Information or Input Similarity</strong>: Knowledge questions related to input requirements on system. </li>
                <li> <strong>Understanding</strong>: Knowledge questions related to system operation. </li>
                <li> <strong>Analysis and Feedback</strong>: Knowledge questions related to the analysis of design documents. </li>
                <li> <strong>Human-Machine Interface</strong>: Complexity of interface and experience utilizing system. </li>
                <li> <strong>Safety Culture and Training</strong>: Related to safety training and culture related the system. </li>
                <li> <strong>Access Control</strong>: Availability of access to the system by plant operators and maintenance staff. </li>
                <li> <strong>Tests</strong>: Validation and verification tests performed for defend against CCFs. </li>
            </ol>
            """
# --- End Template Text ---

# %% --- Tab Text ---
# Section Titles
subfactors = ["Input Similarity", "Understanding", "Analysis and Feedback", "Human-Machine Interface", "Safety Culture and Training", "Access Control", "Tests"]
score_transform = {4:'A', 3:'B', 2:'C', 1:'D', 0:'E', 'A':4, 'B':3, 'C':2, 'D':1, 'E':0}

# Input Similarity
input_sim_qa = {'##### What of Information: What is the information or variable of interest (pressure, temperature, etc.) and is that shared by the members of the CCCG?': 'Considering the elements of the CCCG, to what extent do the elements rely on the same “What” information?',
                '##### Where of Information: Where does the information come from (pressure sensor, human messenger, external system, etc.)  and is that shared by the members of the CCCG? ': 'Considering the elements of the CCCG, to what extent do the elements rely on the same “where” information?',
                '##### Format of Information: What is the format of the information or data and is that the same format employed for all members of the CCCG? ': "Considering the elements of the CCCG, to what extent do the elements rely on the same “format” information?",
                '##### Means of Information: How is the information transferred (wireless, fiberoptic, wired, etc.) and is that the same means employed for all members of the CCCG?': 'Considering the elements of the CCCG, to what extent do the elements rely on the same “how” information?',
                '##### When of Information: When is the information required (i.e. timing of information) and is that the same timing employed for all members of the CCCG?': 'Considering the elements of the CCCG, to what extent do the elements rely on the same “when” information?'}
input_sim_scale = ['Not at all', 'To a small extent', 'To a moderate extent', 'To a great extent', 'Fully and systematically']
input_sim_scale_value = [1., 0.75, 0.5, 0.25, 0.]
input_sim_response_dict = dict(zip(input_sim_scale, input_sim_scale_value))

# Understanding 
understanding_qa = {'Novelty: Considering the elements of the CCCG, to what extent do the elements rely on the novel, principles, configurations, or  information?':['Not Novel: The CCCG elements contain well-understood concepts, reused technology, or similar configurations to previously implemented systems.', 'Novel: The CCCG can be described as first-of-a-kind, software with limited operational experience, or contains concepts that are not fully understood.'],
                    'Complexity: Do the members of the CCCG perform only a single dedicated function/action?':['Yes', 'No'],
                    'Misfit: Do the members of the CCCG ?':["""High Misfit: The system has high "misfit" if the majority of the system's functionality is accomplished through off-the-shelf systems, pre-existing functions, or established functions.""", """Low Misfit: The system has low “misfit” if there are zero to minimal off-the-shelf systems, pre-existing functions, or established functions. (mostly purpose-built functions)."""],
                    'Experience: Indicate the operational experience of the CCCG':['More: Operational experience is more than 10 years.', 'Less: Operational experience is less than 10 years.']
                   }
understanding_score = {'Novel': 1, 'Not Novel': 0,
                       'Yes': 0, 'No': 1,
                       'High Misfit': 0, 'Low Misfit': 1,
                       'More': 0, 'Less': 1}

# Analysis and Feedback
afa_qa = OrderedDict()
afa_qa['Analysis: Indicate the level of risk analysis that was performed for the CCCG'] = ['No-An: The CCCG has not been identified and no CCF analysis has been carried out for the specific CCCG.','An: The CCCG is identified as a potential hazard. Little consideration is made to how a CCF within a CCCG might influence the system.','An+: The CCCG is identified and analyzed for its threat to system performance. CCF is considered. Hazard and consequences are tracked as part of an FTA or other formal PRA tools.']
afa_qa['Feedback: Indicate the level of feedback that was performed for the CCCG'] = ['No-F: No feedback concerning the CCCG was provided to the design team.','F: Feedback was provided to the design team concerning the specific CCCG.','F+: Detailed feedback was provided to the design team. There is evidence that feedback led to actionable recommendations that are document trackable']
afa_qa['Awareness: Indicate the level of awareness of CCF as evident in the design with respect to the CCCG.'] = ['Level 1: There is no evidence of awareness for CCF of the CCCG. No dedicated attempt to prevent software CCF was included in the design (i.e., duplication of software in redundant trains). The CCCG has low levels or no built-in redundancy.','Level 2: There is evidence of general CCF knowledge as demonstrated by the existence of redundant configurations within the design. No diversity is used to support design.','Level 3: There is evidence of awareness of software-based CCFs. Diverse software configurations are used. The analyst may also reason that there are other advanced methods beyond diversity that merit a score beyond Level 2.']

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
hmi_qa = OrderedDict()
hmi_qa['Interaction Frequency: Indicate the level of interaction the user/operator/staff has with the CCCG'] = ['Minimal: Interactions are low or infrequent.', 'Normal: Interactions are regular, normal, scheduled, or routine.']
hmi_qa['Operator/User: Indicate how user/operator interactions are controlled for the CCCG'] = ['No Procedures: There are no written procedures or guidance to interact with the CCCG.', 'Procedures: There are written procedures to control the operation.', 'Checklists: Checklists to compliment procedures.']
hmi_qa['Maintenance: Indicate how maintenance activities are controlled for the CCCG.'] = ['A: No guidance or controls.', 'B: Work checked by a supervisor.', 'C: Post maintenance testing.', 'D: Work checked and tested.', 'E: All maintenance activities have specific acceptance tests.']
hmi_operator_score = {'Normal|No Procedures': 4, 'Minimal|No Procedures': 3, 'Normal|Procedures': 3,  'Minimal|Procedures': 2, 'Normal|Checklists': 1, 'Minimal|Checklists': 0}
hmi_maintenance_score = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'E': 0}

# Safety Culture and Training
culture_qa = OrderedDict()
culture_qa['Training: What level of education has the staff received regarding the components and software of the CCCG?'] = ['On-the-job: No formalized education concerning any aspect of the CCCG.','General: Basic general education concerning the CCCG.','Specialized: Detailed training, and education related to the specific components and software of the CCCG. May include simulator training, when applicable. Also, years of experience may be considered.']
culture_qa['Safety Culture: What level of education has the staff received regarding the components and software of the CCCG?'] = ['Casual: Staff may or may not have safety in mind. No safety training.','Safety Oriented: Staff have safety in mind. Periodic safety training related to working with the components/software of the CCCG.','Safety Oriented+: Staff have safety in mind, there is a clearly defined organizational safety culture, safety policies, regular safety training.']
culture_score = {'Casual': 4, 'Safety Oriented': 2, 'Safety Oriented+': 0, 'On-the-job': 4, 'General': 2, 'Specialized': 0}

# Access Control
control_qa = {'What level of access control is in place for the components and software of the CCCG?':
              ['A: No control, open access networks, unsecured physical locations.',
               'B: Secured physical locations, private networks, general institutional access, multiple unrelated software systems found in single physical location.',
               'C: Secured physical locations, private networks, limited institutional access (e.g., authorized personnel only, and passwords).',
               'D: Secured physical locations, private networks, limited access to authorized and trained personnel only. Close supervision is employed. The area where software is found is limited to software of similar purposes (i.e., multiple software programs on the same machine but all related to similar purpose) multiple systems may be present in the same area.',
               'E: Secured physical locations, private networks, extremely limited access, trained personnel only operating under close supervision, specialized machines (i.e., no other software present), only a single-purpose system is present in the area.']
             }

# Testing
testing_qa = {'What level of testing is planned or has been implemented for the CCCG?':
              ['A: No testing of the system, specifically the CCCG.',
               'B: Individual unit testing (single examples for each software type within CCCG). An example unit has been tested.',
               'C: Detailed testing is performed on an example system (i.e., CCCG). Testing includes verification and compliance testing to ensure the CCCG meets all required criteria as a unit.',
               'D: Commissioning tests performed on the specific CCCG to be employed. Detailed integration testing of the CCCG, in addition to stress testing.',
               'E: In addition to C&D levels, a long-term test is conducted for the CCCG. The test is performed in parallel with existing system for approximately for a specified duration (e.g.,1 year.)']
              }
# --- End Tab ---

# %% --- Function Blocks ---

def transform_data(data):
    """
    Takes a panadas dataframe and, utilizing the above scoring tables, transforms the values into scoring values for calculation.

    Parameters
    ----------
    data : pandas DataFrame
        Dataframe from the uploaded excel file. Single column with the answers selected.

    Returns
    -------
    transformed_data : dict
        Dictionary of subfactors and their scores {"subfactor":"score"}

    """
    master_dict = {}
    
    for d in [culture_score, hmi_maintenance_score, hmi_operator_score, afa_score, understanding_score, understanding_score, input_sim_response_dict]:
        for key, value in d.items():
            if key not in master_dict:
                master_dict[key] = value
    
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
    weight += master_dict[new_values[0]]
    weight += master_dict[new_values[1]]
    weight += master_dict[new_values[2]]
    weight += master_dict[new_values[3]]
    weight += master_dict[new_values[4]]
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
    Ut = master_dict[new_values[5]] + master_dict[new_values[6]] + master_dict[new_values[7]] + master_dict[new_values[8]]
    survey_data["Understanding"] = score_transform[Ut]

    # For Analysis and Feedback
    score = master_dict[new_values[9]]
    survey_data["Analysis and Feedback"] = score

    # For Human-Machine Interface
    m  = max(master_dict[new_values[10]], master_dict[new_values[11]])
    survey_data["Human-Machine Interface"] = score_transform[m]

    # For Safety Culture and Training
    m = max(master_dict[new_values[12]], master_dict[new_values[13]])
    score = score_transform[m]
    survey_data["Safety Culture and Training"] = score

    # For Access Control
    survey_data["Access Control"] = new_values[14]

    # For Tests
    survey_data["Tests"] = new_values[15]
    
    return survey_data

def CCGS_persistence():
    # Persistent page assets
    if "CCGS_tasks" not in st.session_state:
        st.session_state.CCGS_tasks = None
        st.session_state.CCGS_uploaded_file_data = None
        st.session_state.CCGS_uploaded_file_name = None
        st.session_state.CCGS_uploaded_file_type = None

    if "CCGS_submitted" not in st.session_state:
        st.session_state.CCGS_submitted = False


def download_template():
    st.text("Click below to download a template to input Common Cause Evaluation data.")

    df_QA = pd.DataFrame({
        "Questions": questions,
        "Answers": answers
    })

    df_dropdown = pd.DataFrame({"Dropdown Values": dropdown_values})

    xlsx_data = df_QA.to_csv(index=False)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_QA.to_excel(writer, sheet_name="Questions", index=False)
        df_dropdown.to_excel(writer, sheet_name="Dropdowns", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Questions"]

        # Range for dropdown for each equestion
        Q1 = "Dropdowns!$A$2:$A$6"
        Q2 = "Dropdowns!$A$2:$A$6"
        Q3 = "Dropdowns!$A$2:$A$6"
        Q4 = "Dropdowns!$A$2:$A$6"
        Q5 = "Dropdowns!$A$2:$A$6"
        Q6 = "Dropdowns!$A$7:$A$8"
        Q7 = "Dropdowns!$A$9:$A$10"
        Q8 = "Dropdowns!$A$11:$A$12"
        Q9 = "Dropdowns!$A$13:$A$14"
        Q10 = "Dropdowns!$A$15:$A$17"
        Q11 = "Dropdowns!$A$18:$A$20"
        Q12 = "Dropdowns!$A$21:$A$23"
        Q13 = "Dropdowns!$A$24:$A$25"
        Q14 = "Dropdowns!$A$26:$A$28"
        Q15 = "Dropdowns!$A$29:$A$33"
        Q16 = "Dropdowns!$A$34:$A$36"
        Q17 = "Dropdowns!$A$37:$A$39"
        Q18 = "Dropdowns!$A$29:$A$33"
        Q19 = "Dropdowns!$A$29:$A$33"

        worksheet.data_validation(
            1, 1, 1, 1, {"validate": "list", "source": Q1})
        worksheet.data_validation(
            2, 1, 2, 1, {"validate": "list", "source": Q2})
        worksheet.data_validation(
            3, 1, 3, 1, {"validate": "list", "source": Q3})
        worksheet.data_validation(
            4, 1, 4, 1, {"validate": "list", "source": Q4})
        worksheet.data_validation(
            5, 1, 5, 1, {"validate": "list", "source": Q5})
        worksheet.data_validation(
            6, 1, 6, 1, {"validate": "list", "source": Q6})
        worksheet.data_validation(
            7, 1, 7, 1, {"validate": "list", "source": Q7})
        worksheet.data_validation(
            8, 1, 8, 1, {"validate": "list", "source": Q8})
        worksheet.data_validation(
            9, 1, 9, 1, {"validate": "list", "source": Q9})
        worksheet.data_validation(
            10, 1, 10, 1, {"validate": "list", "source": Q10})
        worksheet.data_validation(
            11, 1, 11, 1, {"validate": "list", "source": Q11})
        worksheet.data_validation(
            12, 1, 12, 1, {"validate": "list", "source": Q12})
        worksheet.data_validation(
            13, 1, 13, 1, {"validate": "list", "source": Q13})
        worksheet.data_validation(
            14, 1, 14, 1, {"validate": "list", "source": Q14})
        worksheet.data_validation(
            15, 1, 15, 1, {"validate": "list", "source": Q15})
        worksheet.data_validation(
            16, 1, 16, 1, {"validate": "list", "source": Q16})
        worksheet.data_validation(
            17, 1, 17, 1, {"validate": "list", "source": Q17})
        worksheet.data_validation(
            18, 1, 18, 1, {"validate": "list", "source": Q18})
        worksheet.data_validation(
            19, 1, 19, 1, {"validate": "list", "source": Q19})

    writer.close()
    xlsx_data = output.getvalue()

    st.download_button(
        label="⬇️ Download Template_CCCG_Survey.xlsx",
        data=xlsx_data,
        file_name="Template_CCCG_Survey.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    return

# Function to clear previous uploaded file if user clicks on the X
def clear_task():
    st.session_state.CCGS_tasks = None

# Function to show previously loaded files
def task_box():
    col1, col2 = st.columns([8, 1])

    with col1:
        st.write(
            f"""
            <div style="padding:10px; 
                        border:1px solid #ccc; 
                        border-radius:5px; 
                        background-color:#f7f7f7;
                        font-weight:600;">
                {st.session_state.CCGS_uploaded_file_name}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.button("✖", key="clear_title_btn", on_click=clear_task)


@st.dialog(title="Analysis & Feedback Selection Error:")
def analysis():
    st.write("You've selected \"No Analysis\" with feedback. It is not possible to have feedback without analysis. Rechoose your \"Analysis\" parameter or select \"No-F\" under \"Feedback\".")

def print_subBeta(beta, sub_beta, software_total_failure):
    for key, val in sub_beta.items():
        sub_beta[key] = val/beta if beta > 0 else 0
    sub_beta_df = pd.DataFrame([{"Subfactor": key, "Relative Contribution": val} for key, val in sub_beta.items()])
    st.divider()
    st.subheader("Subfactor Contributions:")
    try:
        st.dataframe(sub_beta_df, width="stretch", hide_index=True)
        
    # Note: except statement should target the exact exception that occurs. Need to fix.
    except:
        st.dataframe(sub_beta_df, use_container_width=True, hide_index=True)
        
    st.markdown(f"""
                <div style="
                margin-top: 0.5rem;
                padding: 1rem 1.1rem;
                border-radius: 12px;
                background: linear-gradient(135deg, #f4f8fc 0%, #e9f0f7 100%);
                                            border: 1px solid #d6e0ea;
                                            ">
                                            <div style="font-size: 0.85rem; font-weight: 700; color: #516b86; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.65rem;">
                                            Evaluation Summary
                                            </div>
                                            <div style="font-size: 1rem; color: #16324f; margin-bottom: 0.4rem;">
                                            <strong>Beta Factor:</strong> {beta:.3g}
                                            </div>
                                            <div style="font-size: 1rem; color: #16324f;">
                                            <strong>CCCG Failure Probability:</strong> {beta * software_total_failure:.3e}
                                            </div>
                                            </div>
                """,
                              unsafe_allow_html=True,
                              )    
def app():
      CCGS_persistence() 
    
      st.markdown(
          """
          <h2 style="white-space: nowrap; text-align: center; color: #16324f;">
              Common Cause Evaluation
          </h2>
          """,
          unsafe_allow_html=True,
      )
      qa_default_index = 3
      survey_data = {}
      st.markdown(
          """
          <style>
          .stTabs [data-baseweb="tab-list"] {
              flex-wrap: wrap;
              gap: 0.4rem;
              align-items: stretch;
          }
    
          .stTabs [data-baseweb="tab"] {
              white-space: normal;
              min-height: 3rem;
              height: auto;
              padding: 0.35rem 0.8rem;
              line-height: 1.15;
              text-align: center;
              justify-content: center;
              align-items: center;
              display: flex;
              border-radius: 10px 10px 0 0;
              border: 1px solid #d6e0ea;
              background: #eef3f8;
              color: #35506b;
              font-weight: 600;
          }
    
          .stTabs [data-baseweb="tab"]:hover {
              background: #dfeaf4;
              color: #16324f;
          }
    
          .stTabs [data-baseweb="tab"]:nth-of-type(9) {
              background: #e8f4ec;
              color: #1f5f3b;
              border-color: #b9d7c1;
              font-weight: 800;
          }
    
          .stTabs [data-baseweb="tab"]:nth-of-type(9):hover {
              background: #d7ebde;
              color: #15492d;
          }
    
          .stTabs [aria-selected="true"] {
              background: #16324f;
              color: #ffffff;
              border-color: #16324f;
          }
    
          .stTabs [data-baseweb="tab"] p {
              margin: 0;
              font-weight: inherit;
          }
          </style>
          """,
          unsafe_allow_html=True,
      )
      tab_names = [
          'General Information',
          'Information or Input Similarity',
          'Understanding',
          'Analysis and Feedback',
          'Human-Machine Interface',
          'Safety Culture and Training',
          'Access Control',
          'Tests',
          'Calculation Results',
      ]
      tabs = st.tabs(tab_names)
    
      with tabs[0]:
            st.markdown(general_instructions)
        
            st.subheader('Manual Input')
            st.markdown(manual_instructions, unsafe_allow_html=True)
        
            st.subheader('Uploading Information')
            st.markdown("""
                        For uploaded data, the format is the same. There are two columns; column 1 asks the same questions as the web survey. The second column is answers. **Answers are selected from a dropdown menu from each cell. Do not customize the answers.** \n
                        To upload the data, navigate to the Calculation Results tab, enter a software total failure probability, and upload the data. Any answers provided in the manual input tabs are overridden by the uploaded file.  
                        """)
        
            download_template()
    
      with tabs[1]:
            # st.subheader('Information or Input Similarity')
            ind = 0
            weight = 0.0
            score = None
            for key, val in input_sim_qa.items():
                  ind += 1
                  st.markdown(key)
                  response = st.radio(val, input_sim_scale, horizontal=True, key='input_sim' + str(ind), index=qa_default_index)
                  weight += input_sim_response_dict[response]
        
            ave = weight / ind
            # ToDo: need to align with CCF paper
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
    
      headers = tab_names[2:8]
      #headers = ['Understanding', 'Analysis and Feedback', 'Human-Machine Interface', 'Safety Culture and Training', 'Access Control', 'Tests']

      qa = [understanding_qa, afa_qa, hmi_qa, culture_qa, control_qa, testing_qa]
      for tab, h, q in zip(tabs[2:], headers, qa):
            with tab:
                  # st.subheader(h)
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
                        if len(options) == 0: options = val
                        if len(captions) == 0: captions = None
                
                        r = st.radio(k, options, captions=captions, horizontal=False, key=h + str(ind), index=1)
                        response.append(r)
        
                  if h == 'Understanding':
                        Ut = np.sum([understanding_score[k] for k in response])
                        score = score_transform[Ut]
            
                  elif h == 'Analysis and Feedback':
                        name = '|'.join(response)
                        if afa_score[name] != None:
                            score = afa_score[name]
                        else:
                            analysis()
            
                  elif h == 'Human-Machine Interface':
                        op = '|'.join(response[0:2])
                        mt = response[2]
                        s1 = hmi_operator_score[op]
                        s2 = hmi_maintenance_score[mt]
                        smax = max(s1, s2)
                        score = score_transform[smax]
            
                  elif h == 'Safety Culture and Training':
                        cul = culture_score[response[0]]
                        ed = culture_score[response[1]]
                        m = max(cul, ed)
                        score = score_transform[m]
            
                  else:
                      score = response[0]
                  
                  survey_data[h] = score
    
      with tabs[-1]:              
          st.caption("Set the survey configuration and run the evaluation.")
          software_total_failure = st.number_input('Software Total Failure Probability', value=1.0e-4, format='%.2e', key="sfp")
        
          with st.form("CCCGS_opener"):             
              try:
                  submitted = st.form_submit_button("Evaluate", type="primary", width="stretch", hide_index=True)
              except:
                  submitted = st.form_submit_button("Evaluate", type="primary", use_container_width=True)                  
        
              if submitted == True:
                  st.session_state.CCGS_submitted = submitted
        
          uploaded = st.file_uploader('Upload your data', type=['xlsx'], key="CCGS_uploader")

          if st.session_state.CCGS_tasks != None and uploaded == None:
              # Show last uploaded file with option to remove
              st.session_state.CCGS_uploaded_file_data = st.session_state.CCGS_tasks.read()
              st.session_state.CCGS_uploaded_file_name = st.session_state.CCGS_tasks.name
              st.session_state.CCGS_uploaded_file_type = st.session_state.CCGS_tasks.type
              task_box()
          else:
              # Overwrite stored information
              st.session_state.CCGS_tasks = uploaded 
        
          if st.session_state.CCGS_submitted and st.session_state.CCGS_tasks == None:
              beta, sub_beta = compute_beta(survey_data)
              print_subBeta(beta, sub_beta, software_total_failure)
                 
          elif st.session_state.CCGS_submitted and st.session_state.CCGS_tasks != None:
              survey_data = st.session_state.CCGS_tasks
              survey_data = pd.read_excel(survey_data, usecols=[1], sheet_name="Questions", engine="openpyxl")
              survey_data = transform_data(survey_data)
                  
              beta, sub_beta = compute_beta(survey_data)
              print_subBeta(beta, sub_beta, software_total_failure)