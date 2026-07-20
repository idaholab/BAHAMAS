# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 11:35:39 2026

@author: CHENE
"""

import pandas as pd
import numpy as np
from scipy import interpolate
from scipy.stats import loguniform
from bahamas.software_total_failure_probability_bbn import BBN
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
workdir = os.path.dirname(__file__)
defect_data = os.path.join(workdir, './Defect_Data.xlsx')

response_scale = [1, 0.75, 0.5, 0.25, 0]
sil_mean = [0.5, 0.05, 0.005, 0.0005, 0.00005]
sil_lower = [0.1, 0.01, 0.001, 0.0001, 0.00001]
sil_upper = [1, 0.1, 0.01, 0.001, 0.0001]

interp_mean = interpolate.interp1d(response_scale, np.log(sil_mean), kind='linear')
interp_lower = interpolate.interp1d(response_scale, np.log(sil_lower), kind='linear')
interp_upper = interpolate.interp1d(response_scale, np.log(sil_upper), kind='linear')


# Response scale in dictionary
response_scale       = ['Not at all or to a partial extent', 'To a small extent', 'To a moderate extent', 'To a great extent', 'Fully and systematically']
response_index       = [0, 1, 2, 3, 4]
response_ref         = dict(zip(response_scale, response_index))
response_scale_value = [1., 0.75, 0.5, 0.25, 0.]
response_dict        = dict(zip(response_scale, response_scale_value))


def get_sil_val(scale):
  mean =  np.exp(interp_mean(scale))
  lower = np.exp(interp_lower(scale))
  upper = np.exp(interp_upper(scale))
  return lower, mean, upper


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

all_qa_dicts = [concept_qa, requirement_qa, design_qa, implementation_qa, testing_qa, InM_qa]
all_wt_dicts = [concept_weight, requirement_weight, design_weight, implementation_weight, testing_weight, InM_weight]
    
load_data = "./Template_SoftwareQuality_Survey.xlsx"

survey_data = pd.read_excel(load_data, sheet_name="Questions", engine="openpyxl")

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
             concept_samples.append(loguniform.rvs(a, b, size=10) * weight)

        elif cat == "Requirement":
             weight = get_weight(row, requirement_qa, requirement_weight)[safety_ind]
             sum_r += weight
             a, mean, b = get_sil_val(response_dict[val])
             requirement_samples.append(loguniform.rvs(a, b, size=10) * weight)
                            
        elif cat == "Design":
             weight = get_weight(row, design_qa, design_weight)[safety_ind]
             sum_d += weight
             a, mean, b = get_sil_val(response_dict[val])
             design_samples.append(loguniform.rvs(a, b, size=10) * weight)

        elif cat == "Implementation":
             weight = get_weight(row, implementation_qa, implementation_weight)[safety_ind]
             sum_i += weight
             a, mean, b = get_sil_val(response_dict[val])
             implementation_samples.append(loguniform.rvs(a, b, size=10) * weight)

        elif cat == "Testing":
             weight = get_weight(row, testing_qa, testing_weight)[safety_ind]
             sum_t += weight
             a, mean, b = get_sil_val(response_dict[val])
             testing_samples.append(loguniform.rvs(a, b, size=10) * weight)

        elif cat == "Install and Maintenance":
             weight = get_weight(row, InM_qa, InM_weight)[safety_ind]
             sum_InM += weight
             a, mean, b = get_sil_val(response_dict[val])
             InM_samples.append(loguniform.rvs(a, b, size=10) * weight)
            
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
    
def get_weight(user_input, qa, weight):
    # Get question 
    cat      = user_input["Stage"]
    question = user_input["Questions"]
        
    for cat, cat_question in qa.items():
        if cat_question == question: 
            return weight.get(cat)
    return None            

ret = transform_data(survey_data, 1)

sdlc_stages = ['Concept', 'Requirement', 'Design', 'Implementation', 'Testing', 'Install and Maintenance']
sdlc_weight = [1/6]*6
software_survey_data = dict.fromkeys(sdlc_stages, None)

for i, stage in enumerate(sdlc_stages):
    software_survey_data[stage] = {'samples':ret[i]*sdlc_weight[i], 'review':2, 'trigger':1}
    
tasks = None
software_BBN = BBN(defect_data, tasks, data=software_survey_data, num_samples=10, approx=True)
          
runAndPlot(software_BBN)
          
