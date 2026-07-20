# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

'''
Name of Tab on Webpage: Software Quality Survey
'''

# built-in libraries
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from io import BytesIO

# implicit libraries
from scipy.stats import loguniform
import streamlit as st
import numpy as np
import pandas as pd

# explicit libraries
from .regression import get_sil_val
from bahamas.utils import UCA_types
from bahamas.software_total_failure_probability_bbn import BBN

# Reference data location for defect correlations
workdir = os.path.dirname(__file__)
defect_data = os.path.join(workdir, '..', '..', 'data', 'Defect_Data.xlsx')
                
# Response scale in dictionary
response_scale       = ['Not at all or to a partial extent', 'To a small extent', 'To a moderate extent', 'To a great extent', 'Fully and systematically']
response_index       = [0, 1, 2, 3, 4]
response_ref         = dict(zip(response_scale, response_index))
response_scale_value = [1., 0.75, 0.5, 0.25, 0.]
response_dict        = dict(zip(response_scale, response_scale_value))

# SDLC scale in dictionary
sdlc_stages = ['Concept', 'Requirement', 'Design', 'Implementation', 'Testing', 'Install and Maintenance']
sdlc_weight = [1/6]*6
software_survey_data = dict.fromkeys(sdlc_stages, None)

general_instructions = """
                       The Software Quality Survey is a preliminary assessment method to give the user an idea of the current quality of their SDLC without having to invest significant time into process analysis. There are two methods to input the data for the Software Quality survey. Option 1, manually inputting the data using the provided web interface. Option 2, uploading an Excel file covering the same questions. 
                       """

#%% Descriptors
concept_weight          = {'Project management (Concept)': [1, 0.154],
                           'Documentation (Concept)':[1, 0.154],
                           'Separation of safety and non-safety (Concept)':[0.75, 0.115],
                           'Structured specification (Concept)':[0.75, 0.115],
                           'Inspection of specification (Concept)': [0.15, 0.115],
                           'Semi-formal methods (Concept)': [0.15, 0.115],
                           'Formal methods (Concept)': [0.1, 0.077],
                           'Checklists (Concept)': [0.1, 0.077],
                           'Computer-aided specification tools (Concept)': [0.1, 0.077]}

concept_qa             = {'Project management (Concept)': 'To what extent during the conceptual stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
                          'Documentation (Concept)':'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the system design requirements during the conceptual stage activities of the SDLC?',
                          'Separation of safety and non-safety (Concept)':'To what extent did the project define system design requirements during the conceptual stage activities of the SDLC that ensured a clear and deliberate separation between safety-related and non-safety-related functions to prevent unintended interactions and simplify verification and testing?',
                          'Structured specification (Concept)':'To what extent did the project define system design requirements during the conceptual stage activities of the SDLC using a structured, hierarchical approach that decomposed functions into clear, manageable parts and minimized interface complexity?',
                          'Inspection of specification (Concept)': 'To what extent did the project conduct independent inspections of the system design requirements to verify completeness, consistency, and coverage of all relevant safety and technical aspects during the conceptual stage activities of the SDLC?',
                          'Semi-formal methods (Concept)': 'To what extent did the project apply semi-formal methods—such as state machines, sequence diagrams, or data flow diagrams, etc.—to define system design requirements during the conceptual stage activities of the SDLC in a clear, consistent, and analyzable manner?',
                          'Formal methods (Concept)': 'To what extent did the project apply formal methods during the conceptual stage activities of the SDLC?',
                          'Checklists (Concept)': 'To what extent did the project incorporate structured checklists to manage and evaluate during the concept stage of the SDLC, ensuring that critical aspects are systematically considered, interpreted appropriately, and documented with clear justification for any additions or omissions?',
                          'Computer-aided specification tools (Concept)': 'To what extent did the project use computer-aided specification tools—such as model-based editors, structured analysis environments, or specification databases—during the conceptual stage activities of the SDLC to support the creation, organization, and validation of system design requirements in a way that improve consistency, traceability, completeness, and ease of review?'}

requirement_weight     = {'Project management (Requirement)': [1, 0.154],
                           'Documentation (Requirement)':[1, 0.154],
                           'Separation of safety and non-safety (Requirement)':[0.75, 0.115],
                           'Structured specification (Requirement)':[0.75, 0.115],
                           'Inspection of specification (Requirement)': [0.15, 0.115],
                           'Semi-formal methods (Requirement)': [0.15, 0.115],
                           'Formal methods (Requirement)': [0.1, 0.077],
                           'Checklists (Requirement)': [0.1, 0.077],
                           'Computer-aided specification tools (Requirement)': [0.1, 0.077]}


requirement_qa         = {'Project management (Requirement)': 'To what extent during the requirement stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
                          'Documentation (Requirement)':'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the system design requirements during the requirement stage activities of the SDLC?',
                          'Separation of safety and non-safety (Requirement)':'To what extent did the project define system design requirements during the requirement stage activities of the SDLC that ensured a clear and deliberate separation between safety-related and non-safety-related functions to prevent unintended interactions and simplify verification and testing?',
                          'Structured specification (Requirement)':'To what extent did the project define system design requirements during the requirement stage activities of the SDLC using a structured, hierarchical approach that decomposes functions into clear, manageable parts and minimized interface complexity?',
                          'Inspection of specification (Requirement)': 'To what extent did the project conduct independent inspections of the system design requirements to verify completeness, consistency, and coverage of all relevant safety and technical aspects during the requirement stage activities of the SDLC?',
                          'Semi-formal methods (Requirement)': 'To what extent did the project apply semi-formal methods—such as state machines, sequence diagrams, data flow diagrams, etc.—to define system design requirements during the requirement stage activities of the SDLC in a clear, consistent, and analyzable manner?',
                          'Formal methods (Requirement)': 'To what extent did the project apply formal methods during the requirement stage activities of the SDLC?',
                          'Checklists (Requirement)': 'To what extent did the project incorporate structured checklists to manage and evaluate during the requirement stage of the SDLC, ensuring that critical aspects are systematically considered, interpreted appropriately, and documented with clear justification for any additions or omissions?',
                          'Computer-aided specification tools (Requirement)': 'To what extent did the project use computer-aided specification tools—such as model-based editors, structured analysis environments, or specification databases—during the requirement stage activities of the SDLC to support the creation, organization, and validation of system design requirements in a way that improve consistency, traceability, completeness, and ease of review?'}

design_weight         =  {'Observance of guidelines and standards (Design)': [1, 0.121],
                          'Project management (Design)': [1, 0.121],
                          'Documentation (Design)':[1, 0.121],
                          'Structured design (Design)':[0.75, 0.091],
                          'Modularization (Design)':[0.75, 0.091],
                          'Use of well-tried components (Design)': [0.0714, 0.061],
                          'Semi-formal methods (Design)': [0.107, 0.091],
                          'Checklists (Design)': [0.0714, 0.061],
                          'Computer-aided design tools (Design)': [0.70714, 0.061],
                          'Simulation (Design)': [0.0714, 0.061],
                          'Inspection or walkthrough (Design)': [0.0714, 0.061],
                          'Formal methods (Design)': [0.0714, 0.061]}

design_qa              = {'Observance of guidelines and standards (Design)': 'To what extent did the project, during the system design and development stage, adhere to applicable guidelines and standards—whether universally valid, project-specific, or phase-specific—in order to promote failure-free safety-related systems and facilitate effective safety validation?',
                          'Project management (Design)': 'To what extent during the design stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
                          'Documentation (Design)': 'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the system design requirements during the design stage activities of the SDLC?',
                          'Structured design (Design)': 'To what extent did the project apply structured design principles during the design stage activities of the SDLC, including the use of hierarchical decomposition, clearly defined module interfaces, and systematic organization of data and control flows, in order to reduce design complexity, minimize interface-related failures, and support effective verification and validation activities?',
                          'Modularization (Design)': 'To what extent did the project apply modularization during the design stage activities of the SDLC by defining subsystems with limited size, minimizing the complexity and cross-dependencies of interfaces, and clearly specifying the functions and boundaries of each module to reduce design complexity and prevent interface-related failures?',
                          'Use of well-tried components (Design)': 'To what extent did the project incorporate well-tried components during the design stage activities of the SDLC, selecting elements with a proven history of reliable operation and suitability for safety-related applications, in order to reduce the likelihood of first-time faults and enhance confidence in system integrity?',
                          'Semi-formal methods (Design)': 'To what extent did the project apply semi-formal methods—such as state machines, sequence diagrams, or data flow diagrams, etc.—to define system design requirements during the design stage activities of the SDLC in a clear, consistent, and analyzable manner?',
                          'Checklists (Design)': 'To what extent did the project incorporate structured checklists to manage and evaluate during the design stage of the SDLC, ensuring that critical aspects are systematically considered, interpreted appropriately, and documented with clear justification for any additions or omissions?',
                          'Computer-aided design tools (Design)': 'To what extent did the project utilize computer-aided design (CAD) tools during the design stage activities of the SDLC to systematically support hardware and software design?',
                          'Simulation (Design)': 'To what extent did the project use simulation during the design stage activities of the SDLC to systematically and comprehensively evaluate the functional performance of safety-related hardware and software by modeling their behavior under representative conditions using software-based behavioral models?',
                          'Inspection or walkthrough (Design)': 'To what extent did the project apply structured inspections or walkthroughs during the design stage activities of the SDLC to systematically evaluate whether the implementation of safety-related functions conformed to the specification, by having independent reviewers or developers examine the design or code to identify discrepancies, uncertainties, or potential weaknesses for resolution?',
                          'Formal methods (Design)': 'To what extent did the project apply formal methods during the design stage activities of the SDLC?'}

implementation_weight  = {'Functional testing (Implementation)':[1, 1/5],
                          'Project management (Implementation)': [1, 1/5],
                          'Documentation (Implementation)': [1, 1/5],
                          'Black-box testing (Implementation)': [0.25, 2/15],
                          'Field experience (Implementation)': [0.25, 2/15],
                          'Statistical testing (Implementation)': [1/6, 2/15]}

implementation_qa      = {'Functional testing (Implementation)': 'To what extent did the project perform functional testing during the implementation stage activities of the SDLC to verify that the implemented functions behaved as specified, by applying representative input data and comparing the observed outputs against the system requirements to identify deviations or incomplete specifications?',
                          'Project management (Implementation)': 'To what extent during the implementation stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
                          'Documentation (Implementation)': 'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the implementation stage activities of the SDLC?',
                          'Black-box testing (Implementation)': 'To what extent did the project apply black-box testing during the implementation stage activities of the SDLC to verify that safety-related functions met their specifications by executing the system with defined input data and evaluating outputs',
                          'Field experience (Implementation)': 'To what extent during the implementation stage activities of the SDLC did the project incorporate field experience by using components or subsystems with documented histories of successful use in similar applications, ensuring that their reliability and behavior under operational conditions were sufficiently demonstrated through evidence such as usage duration, number of deployments, and absence of safety-related failures?',
                          'Statistical testing (Implementation)': 'To what extent did the project apply statistical testing during the implementation stage activities of the SDLC to evaluate the dynamic behavior, utility, and robustness of the safety-related system by executing it with input data sampled according to the expected statistical distribution of real-world operational inputs?'}

testing_weight         = {"Functional testing (Testing)": [0.75, 3/38],
                          "Functional testing under environmental conditions (Testing)": [0.75, 3/38],
                          "Interference surge immunity testing (Testing)": [0.75, 3/38],
                          "Fault insertion testing (when required diagnostic coverage >= 90 %) (Testing)": [0.75, 3/38],
                          "Project management (Testing)": [1, 4/38],
                          "Documentation (Testing)": [1, 4/38],
                          "Static analysis, dynamic analysis and failure analysis (Testing)": [0.125, 2/38],
                          "Simulation and failure analysis (Testing)": [0.125, 2/38],
                          "Worst-case analysis, dynamic Analysis, and failure analysis (Testing)": [0.125, 2/38],
                          "Static analysis and failure analysis (Testing)": [0.125, 0],
                          "Expanded functional testing (Testing)": [0.125, 4/38],
                          "Black-box testing (Testing)": [1/12, 2/38],
                          "Fault insertion testing (when required diagnostic coverage < 90 %) (Testing)": [1/12, 2/38],
                          "Statistical testing (Testing)": [1/12, 2/38],
                          "Worst-case testing (Testing)": [1/12, 2/38],
                          "Field experience (Testing)": [1/12, 0]}

testing_qa             = {"Functional testing (Testing)": 'To what extent did the project perform functional testing during the testing stage activities of the SDLC to verify that the implemented functions behaved as specified, by applying representative input data and comparing the observed outputs against the system requirements to identify deviations or incomplete specifications?',
                          "Functional testing under environmental conditions (Testing)": 'To what extent during the testing stage activities of the SDLC did the project perform functional testing under environmental conditions to verify that safety-related functions operate reliably when subjected to environmental influences such as temperature, humidity, vibration, or electromagnetic interference, in accordance with relevant standards or representative field conditions?',
                          "Interference surge immunity testing (Testing)": 'To what extent during the testing stage activities of the SDLC did the project perform interference surge immunity testing to verify that safety-related functions remain reliable when subjected to standard surge disturbances on power, signal, and communication lines, simulating real-world electrical interference conditions?',
                          "Fault insertion testing (when required diagnostic coverage >= 90 %) (Testing)": 'To what extent during the testing stage activities (when required diagnostic coverage >= 90 %) of the SDLC did the project apply fault insertion testing to assess the dependability of the safety-related system by deliberately introducing or simulating faults—such as power loss, short circuits, or component failures—and observing the system’s response to ensure it transitions to or maintains a safe state?',
                          "Project management (Testing)": 'To what extent during the testing stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
                          "Documentation (Testing)": 'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the testing stage activities of the SDLC?',
                          "Static analysis, dynamic analysis and failure analysis (Testing)": """To what extent during the testing stage activities of the SDLC did the project apply static analysis, dynamic analysis, and failure analysis to ensure conformance with safety requirements by:
                          1)	systematically reviewing the prototype’s static characteristics—such as data flow consistency, control paths, interface behavior, and adherence to design guidelines—without execution (static),
                          2)	subjecting a near-operational prototype to representative input data to observe whether its behavior aligns with specified requirements (dynamic), and
                          3)	identifying and evaluating potential failure modes and their effects on system safety and performance (failure analysis)?"
                          """,
                          "Simulation and failure analysis (Testing)": """To what extent did the project apply simulation and failure analysis during the testing stage activities of the SDLC to evaluate the safety-related system by:
                          1)	using software-based behavioral models to systematically simulate system functionality under representative conditions (simulation), and
                          2)	identifying and analyzing potential failure modes, their causes, and their effects on system behavior and safety performance (failure analysis)
                          """,
                          "Worst-case analysis, dynamic Analysis, and failure analysis (Testing)": """To what extent did the project apply worst-case analysis, dynamic analysis, and failure analysis during the testing stage activities of the SDLC to ensure the safety-related system met its requirements by:
                          1)	evaluating system behavior under the extreme allowable environmental and operational conditions (worst-case),
                          2)	subjecting a near-operational prototype to representative input data to observe whether its behavior aligns with specified requirements (dynamic), and
                          3)	identifying and evaluating potential failure modes and their effects on system safety and performance (failure analysis)?"
                          """,
                          "Static analysis and failure analysis (Testing)": """To what extent did the project apply static analysis and failure analysis during the testing stage activities of the SDLC to ensure the safety-related system met its requirements by
                          1)	systematically reviewing the prototype's static characteristics—such as data flow consistency, control paths, interface behavior, and adherence to design guidelines—without execution (static),
                          2)	identifying and evaluating potential failure modes and their effects on system safety and performance (failure analysis)?"
                          """,
                          "Expanded functional testing (Testing)": 'To what extent during the testing stage activities of the SDLC did the project apply expanded functional testing to evaluate the behavior of the safety-related system under rare, abnormal, or unspecified input conditions—beyond normal operating scenarios—in order to confirm that the system either responds safely or maintains safety even when behavior is not explicitly defined in the specification?',
                          "Black-box testing (Testing)": 'To what extent during the testing stage activities of the SDLC did the project apply black-box testing to evaluate the dynamic behavior, utility, and robustness of the safety-related system by executing it with input data sampled according to the expected statistical distribution of real-world operational inputs?',
                          "Fault insertion testing (when required diagnostic coverage < 90 %) (Testing)": 'To what extent during the testing stage activities (when required diagnostic coverage < 90 %) of the SDLC did the project apply fault insertion testing to assess the dependability of the safety-related system by deliberately introducing or simulating faults—such as power loss, short circuits, or component failures—and observing the system’s response to ensure it transitions to or maintains a safe state?',
                          "Statistical testing (Testing)": 'To what extent during the testing stage activities of the SDLC did the project apply statistical testing to evaluate the dynamic behavior, utility, and robustness of the safety-related system by executing it with input data sampled according to the expected statistical distribution of real-world operational inputs?',
                          "Worst-case testing (Testing)": 'To what extent during the testing stage activities of the SDLC did the project apply worst-case testing to verify that the safety-related system continued to meet its specified performance and safety requirements when subjected to the most extreme permissible environmental and operational conditions, such as maximum temperature, voltage, or load?',
                          "Field experience (Testing)": 'To what extent did the project incorporate relevant field experience—such as operational history, failure data, and performance records from similar systems—into the testing stage activities of the SDLC to validate assumptions, identify potential weaknesses, and improve the reliability and safety of the final design?'}

InM_weight             = {"Operation and maintenance instructions (Install and Maintenance)": [0.75, 1/9],
                          "User friendliness (Install and Maintenance)": [0.75, 1/9],
                          "Maintenance friendliness (Install and Maintenance)": [0.75, 1/9],
                          "Project management (Install and Maintenance)": [1, 1/9],
                          "Documentation (Install and Maintenance)": [1, 1/9],
                          "Limited operation possibilities (Install and Maintenance)": [0.25, 1/9],
                          "Protection against operator mistakes (Install and Maintenance)": [0.25, 1/9],
                          "Operation only by skilled operators (Install and Maintenance)": [0.25, 1/9],
                          "Functional testing (Install and Maintenance)": [1, 1/9],
                          "Black-box testing (Install and Maintenance)":[1/6, 1/9],
                          "Field experience (Install and Maintenance)":[1/6, 1/9],
                          "Statistical testing (Install and Maintenance)":[1/6, 1/9]}
    
InM_qa                 = {"Operation and maintenance instructions (Install and Maintenance)": 'To what extent did the project employ operation and maintenance instructions—providing essential information on how to use, maintain, and, where applicable, install the safety-related system—during the implementation and maintenance stage activities of the SDLC to help prevent operational and maintenance errors?',
                          "User friendliness (Install and Maintenance)": 'To what extent did the project employ user friendliness concepts in the design to reduce the potential for operator error, minimize the need for intervention, simplify necessary actions, ensuring ergonomic and intuitive interactions, and providing consideration of extreme conditions?',
                          "Maintenance friendliness (Install and Maintenance)": 'To what extent did the project employ maintenance friendliness in the design—by minimizing the need for safety-related maintenance, providing sufficient and easy-to-use diagnostic tools and interfaces, and ensuring that all necessary tools and procedures were available and practical?',
                          "Project management (Install and Maintenance)": 'To what extent during the installation and maintenance stage activities of the SDLC did the project establish and follow structured project management practices, including defined roles and responsibilities, independent quality assurance, formal inspection procedures, configuration management, and the use of standardized guidelines and tools?',
                          "Documentation (Install and Maintenance)": 'To what extent did the project generate and maintain structured, traceable, and lifecycle-aligned documentation that clearly supports the development, verification, and justification of the installation and maintenance stage activities of the SDLC?',
                          "Limited operation possibilities (Install and Maintenance)": 'To what extent were user/maintenance operational modes, switches, elements, configurations limited or controlled?',
                          "Protection against operator mistakes (Install and Maintenance)": 'To what extent were protections ensured to protect the system against operator mistakes such as inputs at the wrong time, value, etc.?',
                          "Operation only by skilled operators (Install and Maintenance)": 'To what extent is the system protected from operation by those lacking appropriate training, skill, or know-how?',
                          "Functional testing (Install and Maintenance)": 'To what extent did the project perform functional testing during the installation and maintenance stage activities of the SDLC to verify that the implemented functions behaved as specified, by applying representative input data and comparing the observed outputs against the system requirements to identify deviations or incomplete specifications?',
                          "Black-box testing (Install and Maintenance)":'To what extent did the project apply black-box testing during the installation and maintenance stage activities of the SDLC to verify that safety-related functions met their specifications by executing the system with defined input data and evaluating outputs?',
                          "Field experience (Install and Maintenance)":'To what extent during the installation and maintenance stage activities of the SDLC did the project incorporate field experience by using components or subsystems with documented histories of successful use in similar applications, ensuring that their reliability and behavior under operational conditions were sufficiently demonstrated through evidence such as usage duration, number of deployments, and absence of safety-related failures?',
                          "Statistical testing (Install and Maintenance)":'To what extent did the project apply statistical testing during the installation and maintenance stage activities of the SDLC to evaluate the dynamic behavior, utility, and robustness of the safety-related system by executing it with input data sampled according to the expected statistical distribution of real-world operational inputs?'}

# %% --- Download Template Text ---
all_qa_dicts = [concept_qa, requirement_qa, design_qa, implementation_qa, testing_qa, InM_qa]
questions = []
for d in all_qa_dicts:
    questions.extend(d.values())

stages = ["Concept"] * len(concept_qa) + ["Requirement"] * len(requirement_qa) + ["Design"] * len(design_qa) + ["Implementation"] * len(implementation_qa) + ["Testing"] * len(testing_qa) + ["Install and Maintenance"] * len(InM_qa) 
answers = ["To a great extent"] * len(questions)
dropdown_values = response_scale
manual_instructions = """
                        For manual input, navigate and complete the survey across the below tabs:
                        <ol>
                            <li> <strong>Concept</strong>: First phase of the SDLC where initial ideas of the system are collected. </li>
                            <li> <strong>Requirement</strong>: Second phase, where specific requirements of system function are described. </li>
                            <li> <strong>Design</strong>: Also known as detailed design, where design details of specified requirements are described. </li>
                            <li> <strong>Implementation</strong>: Phase where the design is implemented in software or hardware. </li>
                            <li> <strong>Testing</strong>: Post implementation, this phase is where the system is evaluated for performance. </li>
                            <li> <strong>Install and Maintenance</strong>: This phase describes when the equipment is actually being installed into the plant or system. </li>
                        </ol>
                      """
            
#%% Function Blocks

def section_label(text: str) -> None:
    """Render a compact section heading."""
    st.markdown(
        f"""
        <div style="
            font-size: 1rem;
            font-weight: 600;
            color: #16324f;
            margin: 0.35rem 0 0.6rem 0;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True,
    )

# Function to initialize persistence of data
def SQS_persistence():
    if "SQS_plot_failure" not in st.session_state:
        st.session_state.SQS_plot_failure = False
        
    if "SQS_num_samples" not in st.session_state:
        st.session_state.SQS_num_samples = 10000
        
    if "SQS_submitted" not in st.session_state:
        st.session_state.SQS_submitted = False
    
    if "SQS_safety" not in st.session_state:
        st.session_state.SQS_safety = False
    
    if "SQS_survey" not in st.session_state:
        st.session_state.SQS_survey          = True
        st.session_state.SQS_concept         = {} 
        st.session_state.SQS_requirement     = {}
        st.session_state.SQS_design          = {}
        st.session_state.SQS_implementation  = {}
        st.session_state.SQS_testing         = {}
        st.session_state.SQS_InM             = {}
        
    if "SQS_tasks" not in st.session_state:
        st.session_state.SQS_tasks = None
        st.session_state.SQS_uploaded_file_data = None
        st.session_state.SQS_uploaded_file_name = None
        st.session_state.SQS_uploaded_file_type = None
        
# Function to add persistence to survey values
def SQS_persistence_survey(state_key, section, index):       
    if section == "concept":
        if state_key not in st.session_state.SQS_concept:
            st.session_state.SQS_concept[state_key] = index
    if section == "requirement":
        if state_key not in st.session_state.SQS_requirement:
            st.session_state.SQS_requirement[state_key] = index    
    if section == "design":
        if state_key not in st.session_state.SQS_design:
            st.session_state.SQS_design[state_key] = index
    if section == "implementation":
        if state_key not in st.session_state.SQS_implementation:
            st.session_state.SQS_implementation[state_key] = index
    if section == "testing":
        if state_key not in st.session_state.SQS_testing:
            st.session_state.SQS_testing[state_key] = index
    if section == "inM":
        if state_key not in st.session_state.SQS_InM:
            st.session_state.SQS_InM[state_key] = index
            
# Function to reset submission button status when a change is made in the input
def reset_submission():
    st.session_state.PA_submitted = False
        
# Function to run and plot the output
def runAndPlot(software_BBN):
    # Calculate results
    output = {}
    style = {}
    
    software_BBN.calculate()
    total_failure_mean, total_failure_sigma, _ = software_BBN.get_total_failure_probability()

    output['Total Failure Prob.'] = [total_failure_mean, total_failure_sigma]
    style['Total Failure Prob.'] = "{:.2e}"
    
    for uca in UCA_types:
        mean, sigma, _ = software_BBN.get_uca(uca)
        output[uca] = [mean, sigma]
        style[uca] = "{:.2e}"
        
    df = pd.DataFrame(output, index=['mean', 'std'])
    styled_df = df.style.format(style)
    st.subheader("""Calculation Results""")
    st.info("**Assessment Result ↓**", icon="👋🏾")

    st.dataframe(styled_df)
    # Visualize data
    if st.session_state.SQS_plot_failure:
        fig = software_BBN.plot(save=False, show=False)
        if isinstance(fig, list):
            for f in fig:
                st.plotly_chart(f)
                
def download_template():
    st.text("Click below to download a template to input Common Cause Evaluation data.")

    df_QA = pd.DataFrame({
        "Stage": stages,
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
        for row, data in df_QA.iterrows():
            worksheet.data_validation(row+1, 2, row+1, 2, {"validate": "list", "source": Q1})

    writer.close()
    xlsx_data = output.getvalue()

    st.download_button(
        label="⬇️ Download Template_SoftwareQuality_Survey.xlsx",
        data=xlsx_data,
        file_name="Template_SoftwareQuality_Survey.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    return

def get_weight(user_input, qa, weight):
    # Get question 
    cat      = user_input["Stage"]
    question = user_input["Questions"]
        
    for cat, cat_question in qa.items():
        if cat_question == question: 
            return weight.get(cat)
    return None 

def transform_data(survey_data, safety_ind):
    # Set return variables    
    concept_samples = []
    requirement_samples = []
    design_samples = []
    implementation_samples = []
    testing_samples = []
    InM_samples = []
    
    sum_c = 0
    sum_r = 0
    sum_d = 0
    sum_i = 0
    sum_t = 0
    sum_InM = 0
    
    for _, row in survey_data.iterrows():
        cat = row["Stage"]
        val = row["Answers"]
        if cat == "Concept":
             weight = get_weight(row, concept_qa, concept_weight)[safety_ind]
             sum_c += weight
             a, mean, b = get_sil_val(response_dict[val])
             concept_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)

        elif cat == "Requirement":
             weight = get_weight(row, requirement_qa, requirement_weight)[safety_ind]
             sum_r += weight
             a, mean, b = get_sil_val(response_dict[val])
             requirement_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)
                            
        elif cat == "Design":
             weight = get_weight(row, design_qa, design_weight)[safety_ind]
             sum_d += weight
             a, mean, b = get_sil_val(response_dict[val])
             design_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)

        elif cat == "Implementation":
             weight = get_weight(row, implementation_qa, implementation_weight)[safety_ind]
             sum_i += weight
             a, mean, b = get_sil_val(response_dict[val])
             implementation_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)

        elif cat == "Testing":
             weight = get_weight(row, testing_qa, testing_weight)[safety_ind]
             sum_t += weight
             a, mean, b = get_sil_val(response_dict[val])
             testing_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)

        elif cat == "Install and Maintenance":
             weight = get_weight(row, InM_qa, InM_weight)[safety_ind]
             sum_InM += weight
             a, mean, b = get_sil_val(response_dict[val])
             InM_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)
            
        else:
            print(cat)
            return None

    concept_samples        = 1 - np.prod(1-np.array(concept_samples)/sum_c, axis=0)
    requirement_samples    = 1 - np.prod(1-np.array(requirement_samples)/sum_r, axis=0)
    design_samples         = 1 - np.prod(1-np.array(design_samples)/sum_d, axis=0)
    implementation_samples = 1 - np.prod(1-np.array(implementation_samples)/sum_i, axis=0)
    testing_samples        = 1 - np.prod(1-np.array(testing_samples)/sum_t, axis=0)
    InM_samples            = 1 - np.prod(1-np.array(InM_samples)/sum_InM, axis=0)

    return [concept_samples, requirement_samples, design_samples, implementation_samples, testing_samples, InM_samples]
    

# Function to clear previous uploaded file if user clicks on the X
def clear_task():
    st.session_state.SQS_tasks = None
    st.session_state.submitted = False
    
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
                {st.session_state.SQS_uploaded_file_name}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.button("✖", key="clear_title_btn", on_click=clear_task)
        
def app():
  SQS_persistence()
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
      .stTabs [data-baseweb="tab"]:nth-of-type(2) { color: #0f4c81; }
      .stTabs [data-baseweb="tab"]:nth-of-type(3) { color: #1d6f5f; }
      .stTabs [data-baseweb="tab"]:nth-of-type(4) { color: #8a5a00; }
      .stTabs [data-baseweb="tab"]:nth-of-type(5) { color: #7a1f5c; }
      .stTabs [data-baseweb="tab"]:nth-of-type(6) { color: #7a2e1f; }
      .stTabs [data-baseweb="tab"]:nth-of-type(7) { color: #4b4b9f; }
      .stTabs [data-baseweb="tab"]:nth-of-type(8) { color: #2f4858; }

      .stTabs [data-baseweb="tab"]:nth-of-type(8) {
          background: #e8f4ec;
          color: #1f5f3b;
          border-color: #b9d7c1;
          font-weight: 800;
          margin-top: 0.15rem;
      }

      .stTabs [data-baseweb="tab"]:nth-of-type(8):hover {
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

  tabs = st.tabs(['General Instructions'] + sdlc_stages + ['Calculation Results'])

  qa_default_index = 3

  # General Instructions:
  with tabs[0]:
      st.markdown(general_instructions)
        
      st.subheader('Manual Input')
      st.markdown(manual_instructions, unsafe_allow_html=True)

      st.subheader('Uploading Information')
      st.markdown("""
                For uploaded data, the format is the same. There are three columns; column 1 specifies the lifecycle stage (do not modify); column 2 asks the same questions as the web survey. The third column is answers. **Answers are selected from a dropdown menu from each cell. Do not customize the answers.** \n
                To upload the data, navigate to the Calculation Results tab, enter the total number of samples to draw from, and upload the data. Any answers provided in the manual input tabs are overridden by the uploaded file.  
                """)
        
      download_template()      
      
  # Concept
  with tabs[1]:
      ind = 0
      for key, val in concept_qa.items():
          ind += 1
          state_key = f"concept{ind}"
          SQS_persistence_survey(state_key, section="concept", index=qa_default_index)
          section_label(key) # Display question
          concept[key]   = st.radio(label=val, 
                                    options=response_scale, 
                                    horizontal=True,
                                    key='CT' + str(ind),
                                    index=st.session_state.SQS_concept[state_key])
                                    
          st.session_state.SQS_concept[state_key] = response_ref[concept[key]]

  # Requirement  
  with tabs[2]:
      ind = 0
      for key, val in requirement_qa.items():
          ind += 1
          state_key = f"requirement{ind}"
          SQS_persistence_survey(state_key, section="requirement", index=qa_default_index)
          section_label(key) # Display question
          requirement[key] = st.radio(label=val,
                                      options=response_scale,
                                      horizontal=True,
                                      key='RT' + str(ind),
                                      index=st.session_state.SQS_requirement[state_key])
          st.session_state.SQS_requirement[state_key] = response_ref[requirement[key]]

  # Design
  with tabs[3]:
      ind = 0
      for key, val in design_qa.items():
          ind += 1
          state_key = f"design{ind}"
          SQS_persistence_survey(state_key, section="design", index=qa_default_index)
          section_label(key) # Display question
          design[key] = st.radio(label=val, 
                                 options=response_scale, 
                                 horizontal=True, 
                                 key='DN' + str(ind), 
                                 index=st.session_state.SQS_design[state_key])
          st.session_state.SQS_design[state_key] = response_ref[design[key]]
  
  # Implementation
  with tabs[4]:
      ind = 0
      for key, val in implementation_qa.items():
          ind += 1
          state_key = f"implementation{ind}"
          SQS_persistence_survey(state_key, section="implementation", index=qa_default_index)
          section_label(key) # Display question
          implementation[key] = st.radio(label=val, 
                                         options=response_scale, 
                                         horizontal=True, 
                                         key='IP' + str(ind), 
                                         index=st.session_state.SQS_implementation[state_key])
          st.session_state.SQS_implementation[state_key] = response_ref[implementation[key]]
  
  # Testing
  with tabs[5]:
      ind = 0
      for key, val in testing_qa.items():
          ind += 1
          state_key = f"testing{ind}"
          SQS_persistence_survey(state_key, section="testing", index=qa_default_index)
          section_label(key)
          testing[key] = st.radio(label=val, 
                                  options=response_scale, 
                                  horizontal=True, 
                                  key='TG' + str(ind), 
                                  index=st.session_state.SQS_testing[state_key])
          st.session_state.SQS_testing[state_key] = response_ref[testing[key]]
  
  # Install and Maintenance
  with tabs[6]:
      ind = 0
      for key, val in InM_qa.items():
          ind += 1
          state_key = f"InM{ind}"
          SQS_persistence_survey(state_key, section="inM", index=qa_default_index)
          section_label(key)
          InM[key] = st.radio(label=val, 
                              options=response_scale, 
                              horizontal=True, 
                              key='IM' + str(ind), 
                              index=st.session_state.SQS_InM[state_key])
          st.session_state.SQS_InM[state_key] = response_ref[InM[key]]
  
  # Calculation Results   
  with tabs[-1]:
      # Functions for configure
      st.write("Set the survey configuration and run the evaluation.")
    
      # Number of samples w/ persistence
      st.session_state.SQS_num_samples = st.number_input("Number of samples", value=10000, key="SQS_num", on_change=reset_submission)

      # Plot option checkbox w/ persistence
      st.session_state.SQS_plot_failure = st.checkbox('Visualize', key="SQS_plot", on_change=reset_submission)
    
      # Safety grouping option
      safety_group = st.checkbox('Safety-Related Grouping?', key="SQS_safety", on_change=reset_submission)
    
      with st.form("SQS_user_form"):
          try:
              submitted = st.form_submit_button("Calculate", type="primary", width="stretch", key="SQS_submit")
          except:
              submitted = st.form_submit_button("Calculate", type="primary", use_container_width=True, key="SQS_submit")
          
          if submitted == True:
              st.session_state.SQS_submitted = submitted
      
      uploaded = st.file_uploader('Upload your data', type=['xlsx'], key="SQS_uploader")
      
      if st.session_state.SQS_tasks != None and uploaded == None:
        # Show last uploaded file with option to remove
        st.session_state.SQS_uploaded_file_data = st.session_state.SQS_tasks.read()
        st.session_state.SQS_uploaded_file_name = st.session_state.SQS_tasks.name
        st.session_state.SQS_uploaded_file_type = st.session_state.SQS_tasks.type
        task_box()
      else:
        # Overwrite stored information
        st.session_state.SQS_tasks = uploaded 
        
      # Process data
      if st.session_state.SQS_submitted and st.session_state.SQS_tasks == None:
          st.text("There")
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
              concept_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)
          concept_samples = 1 - np.prod(1-np.array(concept_samples)/sum_c, axis=0)

          sum_r = 0
          for key, val in requirement.items():
              weight = requirement_weight[key][safety_ind]
              sum_r += weight
              a, mean, b = get_sil_val(response_dict[val])
              requirement_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)
          requirement_samples = 1 - np.prod(1-np.array(requirement_samples)/sum_r, axis=0)

          sum_d = 0
          for key, val in design.items():
              weight = design_weight[key][safety_ind]
              sum_d += weight
              a, mean, b = get_sil_val(response_dict[val])
              design_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)
          design_samples = 1 - np.prod(1-np.array(design_samples)/sum_d, axis=0)
    
          sum_i = 0
          for key, val in implementation.items():
              weight = implementation_weight[key][safety_ind]
              sum_i += weight
              a, mean, b = get_sil_val(response_dict[val])
              implementation_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)
          implementation_samples = 1 - np.prod(1-np.array(implementation_samples)/sum_i, axis=0)
    
          sum_t = 0
          for key, val in testing.items():
              weight = testing_weight[key][safety_ind]
              sum_t += weight
              a, mean, b = get_sil_val(response_dict[val])
              testing_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)
          testing_samples = 1 - np.prod(1-np.array(testing_samples)/sum_t, axis=0)
    
          sum_InM = 0
          for key, val in InM.items():
              weight = InM_weight[key][safety_ind]
              sum_InM += weight
              a, mean, b = get_sil_val(response_dict[val])
              InM_samples.append(loguniform.rvs(a, b, size=st.session_state.SQS_num_samples) * weight)
          InM_samples = 1 - np.prod(1-np.array(InM_samples)/sum_InM, axis=0)

          samples = [concept_samples, requirement_samples, design_samples, implementation_samples, testing_samples, InM_samples]
          for i, stage in enumerate(sdlc_stages):
              software_survey_data[stage] = {'samples':samples[i]*sdlc_weight[i], 'review':2, 'trigger':1}
    
          tasks = None
          software_BBN = BBN(defect_data, tasks, data=software_survey_data, num_samples=st.session_state.SQS_num_samples, approx=True)
          
          runAndPlot(software_BBN)
                
      if st.session_state.SQS_submitted and st.session_state.SQS_tasks != None:
          st.text("Here")
          safety_ind = 0 if safety_group == 'Yes' else 1
          survey_data = pd.read_excel(st.session_state.SQS_tasks, sheet_name="Questions", engine="openpyxl")
          samples = transform_data(survey_data, safety_ind)
          
          for i, stage in enumerate(sdlc_stages):
              software_survey_data[stage] = {'samples':samples[i]*sdlc_weight[i], 'review':2, 'trigger':1}
    
          
          tasks = None
          software_BBN = BBN(defect_data, tasks, data=software_survey_data, num_samples=st.session_state.SQS_num_samples, approx=True)
          
          runAndPlot(software_BBN)

if __name__ == "__main__":
    app()