# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
from .regression import get_sil_val
from scipy.stats import loguniform
import numpy as np
import pandas as pd
import os, sys

# Bahamas Module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from bahamas.utils import UCA_types
from bahamas.software_total_failure_probability_bbn import BBN

workdir = os.path.dirname(__file__)
defect_data = os.path.join(workdir, '..', '..', 'data', 'Defect_Data.xlsx')

# Functions for configure
def configure_inputs() -> None:
    """
    Setup and display the main-page input controls.

    This function renders the survey configuration controls
    directly within the main page content area.
    """
    with st.container(border=True):
        st.caption("Set the survey configuration and run the evaluation.")
        with st.form("my_form"):
            # safety_group =  st.radio('Safety related', ['Yes', 'No'], horizontal=True, key='safety_related')
            safety_group = 'Yes'
            num_samples = st.number_input("Number of samples", value=10000)
            plot_failure = st.checkbox('visualize')

            # The Big Red "Submit" Button!
            submitted = st.form_submit_button(
                "Evaluate", type="primary", use_container_width=True)
    return submitted, num_samples, plot_failure, safety_group


review_trigger_factor = np.exp(-8)
response_scale = ['Not at all or to a partial extent', 'To a small extent', 'To a moderate extent', 'To a great extent', 'Fully and systematically']
response_scale_value = [1., 0.75, 0.5, 0.25, 0.]
response_dict = dict(zip(response_scale, response_scale_value))
sdlc_stages = ['Concept', 'Requirement', 'Design', 'Implementation', 'Testing', 'Install and Maintenance']
software_survey_data = dict.fromkeys(sdlc_stages, None)
concept_weight = {'Project management': [1, 0.154],
                  'Documentation':[1, 0.154],
                  'Separation of safety and non-safety':[0.75, 0.115],
                  'Structured specification':[0.75, 0.115],
                  'Inspection of specification': [0.15, 0.115],
                  'Semi-formal methods': [0.15, 0.115],
                  'Formal methods': [0.1, 0.077],
                  'Checklists': [0.1, 0.077],
                  'Computer-aided specification tools': [0.1, 0.077]}
concept_qa = {'Project management': 'To what extent during the conceptual stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
                  'Documentation':'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the system design requirements during the conceptual stage activities of the SDLC?',
                  'Separation of safety and non-safety':'To what extent did the project define system design requirements during the conceptual stage activities of the SDLC that ensured a clear and deliberate separation between safety-related and non-safety-related functions to prevent unintended interactions and simplify verification and testing?',
                  'Structured specification':'To what extent did the project define system design requirements during the conceptual stage activities of the SDLC using a structured, hierarchical approach that decomposed functions into clear, manageable parts and minimized interface complexity?',
                  'Inspection of specification': 'To what extent did the project conduct independent inspections of the system design requirements to verify completeness, consistency, and coverage of all relevant safety and technical aspects during the conceptual stage activities of the SDLC?',
                  'Semi-formal methods': 'To what extent did the project apply semi-formal methods—such as state machines, sequence diagrams, or data flow diagrams, etc.—to define system design requirements during the conceptual stage activities of the SDLC in a clear, consistent, and analyzable manner?',
                  'Formal methods': 'To what extent did the project apply formal methods during the conceptual stage activities of the SDLC?',
                  'Checklists': 'To what extent did the project incorporate structured checklists to manage and evaluate during the concept stage of the SDLC, ensuring that critical aspects are systematically considered, interpreted appropriately, and documented with clear justification for any additions or omissions?',
                  'Computer-aided specification tools': 'To what extent did the project use computer-aided specification tools—such as model-based editors, structured analysis environments, or specification databases—during the conceptual stage activities of the SDLC to support the creation, organization, and validation of system design requirements in a way that improve consistency, traceability, completeness, and ease of review?'}
requirement_weight = concept_weight
requirement_qa = {'Project management': 'To what extent during the requirement stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
                  'Documentation':'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the system design requirements during the requirement stage activities of the SDLC?',
                  'Separation of safety and non-safety':'To what extent did the project define system design requirements during the requirement stage activities of the SDLC that ensured a clear and deliberate separation between safety-related and non-safety-related functions to prevent unintended interactions and simplify verification and testing?',
                  'Structured specification':'To what extent did the project define system design requirements during the requirement stage activities of the SDLC using a structured, hierarchical approach that decomposes functions into clear, manageable parts and minimized interface complexity?',
                  'Inspection of specification': 'To what extent did the project conduct independent inspections of the system design requirements to verify completeness, consistency, and coverage of all relevant safety and technical aspects during the requirement stage activities of the SDLC?',
                  'Semi-formal methods': 'To what extent did the project apply semi-formal methods—such as state machines, sequence diagrams, data flow diagrams, etc.—to define system design requirements during the requirement stage activities of the SDLC in a clear, consistent, and analyzable manner?',
                  'Formal methods': 'To what extent did the project apply formal methods during the requirement stage activities of the SDLC?',
                  'Checklists': 'To what extent did the project incorporate structured checklists to manage and evaluate during the requirement stage of the SDLC, ensuring that critical aspects are systematically considered, interpreted appropriately, and documented with clear justification for any additions or omissions?',
                  'Computer-aided specification tools': 'To what extent did the project use computer-aided specification tools—such as model-based editors, structured analysis environments, or specification databases—during the requirement stage activities of the SDLC to support the creation, organization, and validation of system design requirements in a way that improve consistency, traceability, completeness, and ease of review?'}
design_weight = {'Observance of guidelines and standards': [1, 0.121],
                  'Project management': [1, 0.121],
                  'Documentation':[1, 0.121],
                  'Structured design':[0.75, 0.091],
                  'Modularization':[0.75, 0.091],
                  'Use of well-tried components': [0.0714, 0.061],
                  'Semi-formal methods': [0.107, 0.091],
                  'Checklists': [0.0714, 0.061],
                  'Computer-aided design tools': [0.70714, 0.061],
                  'Simulation': [0.0714, 0.061],
                  'Inspection or walkthrough': [0.0714, 0.061],
                  'Formal methods': [0.0714, 0.061]}
design_qa = {'Observance of guidelines and standards': 'To what extent did the project, during the system design and development stage, adhere to applicable guidelines and standards—whether universally valid, project-specific, or phase-specific—in order to promote failure-free safety-related systems and facilitate effective safety validation?',
                  'Project management': 'To what extent during the design stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
                  'Documentation': 'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the system design requirements during the design stage activities of the SDLC?',
                  'Structured design': 'To what extent did the project apply structured design principles during the design stage activities of the SDLC, including the use of hierarchical decomposition, clearly defined module interfaces, and systematic organization of data and control flows, in order to reduce design complexity, minimize interface-related failures, and support effective verification and validation activities?',
                  'Modularization': 'To what extent did the project apply modularization during the design stage activities of the SDLC by defining subsystems with limited size, minimizing the complexity and cross-dependencies of interfaces, and clearly specifying the functions and boundaries of each module to reduce design complexity and prevent interface-related failures?',
                  'Use of well-tried components': 'To what extent did the project incorporate well-tried components during the design stage activities of the SDLC, selecting elements with a proven history of reliable operation and suitability for safety-related applications, in order to reduce the likelihood of first-time faults and enhance confidence in system integrity?',
                  'Semi-formal methods': 'To what extent did the project apply semi-formal methods—such as state machines, sequence diagrams, or data flow diagrams, etc.—to define system design requirements during the design stage activities of the SDLC in a clear, consistent, and analyzable manner?',
                  'Checklists': 'To what extent did the project incorporate structured checklists to manage and evaluate during the design stage of the SDLC, ensuring that critical aspects are systematically considered, interpreted appropriately, and documented with clear justification for any additions or omissions?',
                  'Computer-aided design tools': 'To what extent did the project utilize computer-aided design (CAD) tools during the design stage activities of the SDLC to systematically support hardware and software design?',
                  'Simulation': 'To what extent did the project use simulation during the design stage activities of the SDLC to systematically and comprehensively evaluate the functional performance of safety-related hardware and software by modeling their behavior under representative conditions using software-based behavioral models?',
                  'Inspection or walkthrough': 'To what extent did the project apply structured inspections or walkthroughs during the design stage activities of the SDLC to systematically evaluate whether the implementation of safety-related functions conformed to the specification, by having independent reviewers or developers examine the design or code to identify discrepancies, uncertainties, or potential weaknesses for resolution?',
                  'Formal methods': 'To what extent did the project apply formal methods during the design stage activities of the SDLC?'}
implementation_weight = {'Functional testing':[1, 1/5],
                          'Project management': [1, 1/5],
                          'Documentation': [1, 1/5],
                          'Black-box testing': [0.25, 2/15],
                          'Field experience': [0.25, 2/15],
                          'Statistical testing': [1/6, 2/15]}
implementation_qa = {'Functional testing': 'To what extent did the project perform functional testing during the implementation stage activities of the SDLC to verify that the implemented functions behaved as specified, by applying representative input data and comparing the observed outputs against the system requirements to identify deviations or incomplete specifications?',
                          'Project management': 'To what extent during the implementation stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
                          'Documentation': 'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the implementation stage activities of the SDLC?',
                          'Black-box testing': 'To what extent did the project apply black-box testing during the implementation stage activities of the SDLC to verify that safety-related functions met their specifications by executing the system with defined input data and evaluating outputs',
                          'Field experience': 'To what extent during the implementation stage activities of the SDLC did the project incorporate field experience by using components or subsystems with documented histories of successful use in similar applications, ensuring that their reliability and behavior under operational conditions were sufficiently demonstrated through evidence such as usage duration, number of deployments, and absence of safety-related failures?',
                          'Statistical testing': 'To what extent did the project apply statistical testing during the implementation stage activities of the SDLC to evaluate the dynamic behavior, utility, and robustness of the safety-related system by executing it with input data sampled according to the expected statistical distribution of real-world operational inputs?'}
testing_weight = {
    "Functional testing": [0.75, 3/38],
    "Functional testing under environmental conditions": [0.75, 3/38],
    "Interference surge immunity testing": [0.75, 3/38],
    "Fault insertion testing (when required diagnostic coverage >= 90 %)": [0.75, 3/38],
    "Project management": [1, 4/38],
    "Documentation": [1, 4/38],
    "Static analysis, dynamic analysis and failure analysis": [0.125, 2/38],
    "Simulation and failure analysis": [0.125, 2/38],
    "Worst-case analysis, dynamic Analysis, and failure analysis": [0.125, 2/38],
    "Static analysis and failure analysis": [0.125, 0],
    "Expanded functional testing": [0.125, 4/38],
    "Black-box testing": [1/12, 2/38],
    "Fault insertion testing (when required diagnostic coverage < 90 %)": [1/12, 2/38],
    "Statistical testing": [1/12, 2/38],
    "Worst-case testing": [1/12, 2/38],
    "Field experience": [1/12, 0]
}

testing_qa = {
    "Functional testing": 'To what extent did the project perform functional testing during the testing stage activities of the SDLC to verify that the implemented functions behaved as specified, by applying representative input data and comparing the observed outputs against the system requirements to identify deviations or incomplete specifications?',
    "Functional testing under environmental conditions": 'To what extent during the testing stage activities of the SDLC did the project perform functional testing under environmental conditions to verify that safety-related functions operate reliably when subjected to environmental influences such as temperature, humidity, vibration, or electromagnetic interference, in accordance with relevant standards or representative field conditions?',
    "Interference surge immunity testing": 'To what extent during the testing stage activities of the SDLC did the project perform interference surge immunity testing to verify that safety-related functions remain reliable when subjected to standard surge disturbances on power, signal, and communication lines, simulating real-world electrical interference conditions?',
    "Fault insertion testing (when required diagnostic coverage >= 90 %)": 'To what extent during the testing stage activities of the SDLC did the project apply fault insertion testing to assess the dependability of the safety-related system by deliberately introducing or simulating faults—such as power loss, short circuits, or component failures—and observing the system’s response to ensure it transitions to or maintains a safe state?',
    "Project management": 'To what extent during the testing stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
    "Documentation": 'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the testing stage activities of the SDLC?',
    "Static analysis, dynamic analysis and failure analysis": """To what extent during the testing stage activities of the SDLC did the project apply static analysis, dynamic analysis, and failure analysis to ensure conformance with safety requirements by:
1)	systematically reviewing the prototype’s static characteristics—such as data flow consistency, control paths, interface behavior, and adherence to design guidelines—without execution (static),
2)	subjecting a near-operational prototype to representative input data to observe whether its behavior aligns with specified requirements (dynamic), and
3)	identifying and evaluating potential failure modes and their effects on system safety and performance (failure analysis)?"
""",
    "Simulation and failure analysis": """To what extent did the project apply simulation and failure analysis during the testing stage activities of the SDLC to evaluate the safety-related system by:
1)	using software-based behavioral models to systematically simulate system functionality under representative conditions (simulation), and
2)	identifying and analyzing potential failure modes, their causes, and their effects on system behavior and safety performance (failure analysis)
""",
    "Worst-case analysis, dynamic Analysis, and failure analysis": """To what extent did the project apply worst-case analysis, dynamic analysis, and failure analysis during the testing stage activities of the SDLC to ensure the safety-related system met its requirements by:
1)	evaluating system behavior under the extreme allowable environmental and operational conditions (worst-case),
2)	subjecting a near-operational prototype to representative input data to observe whether its behavior aligns with specified requirements (dynamic), and
3)	identifying and evaluating potential failure modes and their effects on system safety and performance (failure analysis)?"
""",
    "Static analysis and failure analysis": """To what extent did the project apply static analysis and failure analysis during the testing stage activities of the SDLC to ensure the safety-related system met its requirements by
1)	systematically reviewing the prototype's static characteristics—such as data flow consistency, control paths, interface behavior, and adherence to design guidelines—without execution (static),
2)	identifying and evaluating potential failure modes and their effects on system safety and performance (failure analysis)?"
""",
    "Expanded functional testing": 'To what extent during the testing stage activities of the SDLC did the project apply expanded functional testing to evaluate the behavior of the safety-related system under rare, abnormal, or unspecified input conditions—beyond normal operating scenarios—in order to confirm that the system either responds safely or maintains safety even when behavior is not explicitly defined in the specification?',
    "Black-box testing": 'To what extent during the testing stage activities of the SDLC did the project apply statistical testing to evaluate the dynamic behavior, utility, and robustness of the safety-related system by executing it with input data sampled according to the expected statistical distribution of real-world operational inputs?',
    "Fault insertion testing (when required diagnostic coverage < 90 %)": 'To what extent during the testing stage activities of the SDLC did the project apply fault insertion testing to assess the dependability of the safety-related system by deliberately introducing or simulating faults—such as power loss, short circuits, or component failures—and observing the system’s response to ensure it transitions to or maintains a safe state?',
    "Statistical testing": 'To what extent during the testing stage activities of the SDLC did the project apply statistical testing to evaluate the dynamic behavior, utility, and robustness of the safety-related system by executing it with input data sampled according to the expected statistical distribution of real-world operational inputs?',
    "Worst-case testing": 'To what extent during the testing stage activities of the SDLC did the project apply worst-case testing to verify that the safety-related system continued to meet its specified performance and safety requirements when subjected to the most extreme permissible environmental and operational conditions, such as maximum temperature, voltage, or load?',
    "Field experience": 'To what extent did the project incorporate relevant field experience—such as operational history, failure data, and performance records from similar systems—into the testing stage activities of the SDLC to validate assumptions, identify potential weaknesses, and improve the reliability and safety of the final design?'
}

InM_weight = {"Operation and maintenance instructions": [0.75, 1/9],
              "User friendliness": [0.75, 1/9],
              "Maintenance friendliness": [0.75, 1/9],
              "Project management": [1, 1/9],
              "Documentation": [1, 1/9],
              "Limited operation possibilities": [0.25, 1/9],
              "Protection against operator mistakes": [0.25, 1/9],
              "Operation only by skilled operators": [0.25, 1/9],
              "Functional testing": [1, 1/9],
              "Black-box testing":[1/6, 1/9],
              "Field experience":[1/6, 1/9],
              "Statistical testing":[1/6, 1/9]
            }

InM_qa = {"Operation and maintenance instructions": 'To what extent did the project employ operation and maintenance instructions—providing essential information on how to use, maintain, and, where applicable, install the safety-related system—during the implementation and maintenance stage activities of the SDLC to help prevent operational and maintenance errors?',
              "User friendliness": 'To what extent did the project employ user friendliness concepts in the design to reduce the potential for operator error, minimize the need for intervention, simplify necessary actions, ensuring ergonomic and intuitive interactions, and providing consideration of extreme conditions?',
              "Maintenance friendliness": 'To what extent did the project employ maintenance friendliness in the design—by minimizing the need for safety-related maintenance, providing sufficient and easy-to-use diagnostic tools and interfaces, and ensuring that all necessary tools and procedures were available and practical?',
              "Project management": 'To what extent during the installation and maintenance stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
              "Documentation": 'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the installation and maintenance stage activities of the SDLC?',
              "Limited operation possibilities": 'To what extent were user/maintenance operational modes, switches, elements, configurations limited or controlled?',
              "Protection against operator mistakes": 'To what extent were protections ensured to protect the system against operator mistakes such as inputs at the wrong time, value, etc.?',
              "Operation only by skilled operators": 'To what extent is the system protected from operation by those lacking appropriate training, skill, or know-how?',
              "Functional testing": 'To what extent did the project perform functional testing during the installation and maintenance stage activities of the SDLC to verify that the implemented functions behaved as specified, by applying representative input data and comparing the observed outputs against the system requirements to identify deviations or incomplete specifications?',
              "Black-box testing":'To what extent did the project apply black-box testing during the installation and maintenance stage activities of the SDLC to verify that safety-related functions met their specifications by executing the system with defined input data and evaluating outputs?',
              "Field experience":'To what extent during the installation and maintenance stage activities of the SDLC did the project incorporate field experience by using components or subsystems with documented histories of successful use in similar applications, ensuring that their reliability and behavior under operational conditions were sufficiently demonstrated through evidence such as usage duration, number of deployments, and absence of safety-related failures?',
              "Statistical testing":'To what extent did the project apply statistical testing during the installation and maintenance stage activities of the SDLC to evaluate the dynamic behavior, utility, and robustness of the safety-related system by executing it with input data sampled according to the expected statistical distribution of real-world operational inputs?'}

def app():
  st.markdown(
      """
      <h2 style="white-space: nowrap; text-align: center; color: #16324f;">
          Software Quality Survey
      </h2>
      """,
      unsafe_allow_html=True,
  )

  concept = {}
  requirement = {}
  design = {}
  implementation = {}
  testing = {}
  InM = {}
  review_dict = {}
  trigger_dict = {}

  st.markdown(
      """
      <style>
      .stTabs [data-baseweb="tab-list"] {
          flex-wrap: wrap;
          gap: 0.35rem;
      }

      .stTabs [data-baseweb="tab"] {
          background: #eef3f8;
          border-radius: 10px 10px 0 0;
          padding: 0.5rem 0.9rem;
          color: #35506b;
          font-weight: 600;
          border: 1px solid #d6e0ea;
          justify-content: center;
          text-align: center;
      }

      .stTabs [data-baseweb="tab"]:nth-of-type(1) { color: #0f4c81; }
      .stTabs [data-baseweb="tab"]:nth-of-type(2) { color: #1d6f5f; }
      .stTabs [data-baseweb="tab"]:nth-of-type(3) { color: #8a5a00; }
      .stTabs [data-baseweb="tab"]:nth-of-type(4) { color: #7a1f5c; }
      .stTabs [data-baseweb="tab"]:nth-of-type(5) { color: #7a2e1f; }
      .stTabs [data-baseweb="tab"]:nth-of-type(6) { color: #4b4b9f; }
      .stTabs [data-baseweb="tab"]:nth-of-type(7) { color: #2f4858; }

      .stTabs [data-baseweb="tab"]:nth-of-type(7) {
          background: #e8f4ec;
          color: #1f5f3b;
          border-color: #b9d7c1;
          font-weight: 800;
          margin-top: 0.15rem;
      }

      .stTabs [data-baseweb="tab"]:nth-of-type(7):hover {
          background: #d7ebde;
          color: #15492d;
      }

      .stTabs [aria-selected="true"] {
          background: #16324f;
          color: white !important;
          border-color: #16324f;
      }

      .stTabs [data-baseweb="tab"]:hover {
          background: #dfeaf4;
          color: #16324f;
      }

      .stTabs [data-baseweb="tab"] p {
          margin: 0;
          font-weight: inherit;
      }
      </style>
      """,
      unsafe_allow_html=True,
  )

  tabs = st.tabs(sdlc_stages + ['Calculation Results'])

  qa_default_index = 3

  # Concept
  with tabs[0]:
    ind = 0
    for key, val in concept_qa.items():
      ind += 1
      # st.markdown(f"### **{key}**")
      st.subheader(key)
      concept[key] = st.radio(val, response_scale, horizontal=True, key='concept' + str(ind), index=qa_default_index)
    # st.subheader('Quality of Review Activities')
    # review_dict['Concept'] = st.slider('Average Review Number', 0.0, 5.0, value=2., step=0.01, key="concept_review")
    # trigger_dict['Concept'] = st.slider('Average Trigger Coverage', 0.0, 5.0, value=1., step=0.01, key="concept_trigger")

  with tabs[1]:
    ind = 0
    for key, val in requirement_qa.items():
      ind += 1
      st.subheader(key)
      requirement[key] = st.radio(val, response_scale, horizontal=True, key='requirement' + str(ind), index=qa_default_index)
    # st.subheader('Quality of Review Activities')
    # review_dict['Requirement'] = st.slider('Average Review Number', 0.0, 5.0, value=2., step=0.01, key="requirement_review")
    # trigger_dict['Requirement'] = st.slider('Average Trigger Coverage', 0.0, 5.0, value=1., step=0.01, key="requirement_trigger")

  with tabs[2]:
    ind = 0
    for key, val in design_qa.items():
      ind += 1
      st.subheader(key)
      design[key] = st.radio(val, response_scale, horizontal=True, key='design' + str(ind), index=qa_default_index)
    # st.subheader('Quality of Review Activities')
    # review_dict['Design'] = st.slider('Average Review Number', 0.0, 5.0, value=2., step=0.01, key="design_review")
    # trigger_dict['Design'] = st.slider('Average Trigger Coverage', 0.0, 5.0, value=1., step=0.01, key="design_trigger")

  with tabs[3]:
    ind = 0
    for key, val in implementation_qa.items():
      ind += 1
      st.subheader(key)
      implementation[key] = st.radio(val, response_scale, horizontal=True, key='implementation' + str(ind), index=qa_default_index)
    # st.subheader('Quality of Review Activities')
    # review_dict['Implementation'] = st.slider('Average Review Number', 0.0, 5.0, value=2., step=0.01, key="implementation_review")
    # trigger_dict['Implementation'] = st.slider('Average Trigger Coverage', 0.0, 5.0, value=1., step=0.01, key="implementation_trigger")

  with tabs[4]:
    ind = 0
    for key, val in testing_qa.items():
      ind += 1
      st.subheader(key)
      testing[key] = st.radio(val, response_scale, horizontal=True, key='testing' + str(ind), index=qa_default_index)
    # st.subheader('Quality of Review Activities')
    # review_dict['Testing'] = st.slider('Average Review Number', 0.0, 5.0, value=2., step=0.01, key="testing_review")
    # trigger_dict['Testing'] = st.slider('Average Trigger Coverage', 0.0, 5.0, value=1., step=0.01, key="testing_trigger")

  with tabs[5]:
    ind = 0
    for key, val in InM_qa.items():
      ind += 1
      st.subheader(key)
      InM[key] = st.radio(val, response_scale, horizontal=True, key='InM' + str(ind), index=qa_default_index)
    # st.subheader('Quality of Review Activities')
    # review_dict['Install and Maintenance'] = st.slider('Average Review Number', 0.0, 5.0, value=2., step=0.01, key="InM_review")
    # trigger_dict['Install and Maintenance'] = st.slider('Average Trigger Coverage', 0.0, 5.0, value=1., step=0.01, key="InM_trigger")


  with tabs[6]:
    # st.info("**Assessment Result ↓**", icon="👋🏾")
    submitted, num_samples, plot_failure, safety_group = configure_inputs()
    # process data
    if submitted:
      safety_ind = 0 if safety_group == 'Yes' else 1
      concept_samples = []
      requirement_samples = []
      design_samples = []
      implementation_samples = []
      testing_samples = []
      InM_samples = []
      sum_c = 0
      for key, val in concept.items():
        weight = concept_weight[key][safety_ind]
        sum_c += weight
        a, mean, b = get_sil_val(response_dict[val])
        concept_samples.append(loguniform.rvs(a, b, size=num_samples) * weight)
      concept_samples = 1 - np.prod(1-np.array(concept_samples)/sum_c, axis=0)

      sum_r = 0
      for key, val in requirement.items():
        weight = requirement_weight[key][safety_ind]
        sum_r += weight
        a, mean, b = get_sil_val(response_dict[val])
        requirement_samples.append(loguniform.rvs(a, b, size=num_samples) * weight)
      requirement_samples = 1 - np.prod(1-np.array(requirement_samples)/sum_r, axis=0)

      sum_d = 0
      for key, val in design.items():
        weight = design_weight[key][safety_ind]
        sum_d += weight
        a, mean, b = get_sil_val(response_dict[val])
        design_samples.append(loguniform.rvs(a, b, size=num_samples) * weight)
      design_samples = 1 - np.prod(1-np.array(design_samples)/sum_d, axis=0)

      sum_i = 0
      for key, val in implementation.items():
        weight = implementation_weight[key][safety_ind]
        sum_i += weight
        a, mean, b = get_sil_val(response_dict[val])
        implementation_samples.append(loguniform.rvs(a, b, size=num_samples) * weight)
      implementation_samples = 1 - np.prod(1-np.array(implementation_samples)/sum_i, axis=0)

      sum_t = 0
      for key, val in testing.items():
        weight = testing_weight[key][safety_ind]
        sum_t += weight
        a, mean, b = get_sil_val(response_dict[val])
        testing_samples.append(loguniform.rvs(a, b, size=num_samples) * weight)
      testing_samples = 1 - np.prod(1-np.array(testing_samples)/sum_t, axis=0)

      sum_InM = 0
      for key, val in InM.items():
        weight = InM_weight[key][safety_ind]
        sum_InM += weight
        a, mean, b = get_sil_val(response_dict[val])
        InM_samples.append(loguniform.rvs(a, b, size=num_samples) * weight)
      InM_samples = 1 - np.prod(1-np.array(InM_samples)/sum_InM, axis=0)

      samples = [concept_samples, requirement_samples, design_samples, implementation_samples, testing_samples, InM_samples]
      for i, stage in enumerate(sdlc_stages):
        # software_survey_data[stage] = {'samples':samples[i], 'review':review_dict[stage], 'trigger':trigger_dict[stage]}
        software_survey_data[stage] = {'samples':samples[i], 'review':2, 'trigger':1}

      # call BAHAMAS BBN with approx
      # update initialize_stage to accept distribution directly
      output = {}
      style = {}
      tasks = None
      software_BBN = BBN(defect_data, tasks, data=software_survey_data, num_samples=num_samples, approx=True)
      software_BBN.calculate()
      total_failure_mean, total_failure_sigma, _ = software_BBN.get_total_failure_probability()

      output['Total Failure Prob.'] = [total_failure_mean, total_failure_sigma]
      style['Total Failure Prob.'] = "{:.2e}"
      # st.write('Software total failure:', total_failure_mean, 'with std:', total_failure_sigma)
      for uca in UCA_types:
          mean, sigma, _ = software_BBN.get_uca(uca)
          output[uca] = [mean, sigma]
          style[uca] = "{:.2e}"
      df = pd.DataFrame(output, index=['mean', 'std'])
      styled_df = df.style.format(style)


      st.dataframe(styled_df)
      # visualize data
      if plot_failure:
          fig = software_BBN.plot(save=False, show=False)
          if isinstance(fig, list):
              for f in fig:
                  st.plotly_chart(f)
    else:
        pass

