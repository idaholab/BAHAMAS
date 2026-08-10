# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

'''
Name of Tab on Webpage: Comprehensive Assessment
'''

# built-in libraries
import os, sys
from io import BytesIO
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# implicit libraries
import streamlit as st
from streamlit_extras.bottom_container import bottom
import pandas as pd

# explicit libraries
from bahamas.utils import  UCA_types
from bahamas.software_total_failure_probability_bbn import BBN

# Reference data location for defect correlations
workdir = os.path.dirname(__file__)
defect_data = os.path.join(workdir, '..', '..', 'data', 'Example_ComprehensiveAssessment_Defect_Data.xlsx')

#%% --- Page Overview Text Descriptions ---
page_title="""
           <h2 style="white-space: nowrap; text-align: center; color: #16324f;">
               Comprehensive Assessment
           </h2>
           """
general_instructions = """
    This page enables a comprehensive assessment of the software development lifecycle for failure probability estimation. In summary, the user generates a list SDLC activities with corresponding quality level. There are two input Excel files that can be uploaded to the site; Task Data and Defect Data.

    Under Task Data, the Excel file should contain:
        <ul>
            <li> **Task Number**: Standard natural number </li>
            <li> **Human Error Mode**: Select a predefined HEM from the BAHAMAS manual. Defined as D1, D2, O, C, or any combination of modes. A full list can be found in ```Template_Defect_Data.xlsx``` template below under HEMD tab. </li>
            <li> **Review Number**: Float value (e.g., 2 for 2 full-time reviewers or 1.5 for 1 full-time reviewer and  1 half-time reviewer), must be greater than 0. Represents how many qualified individuals have reviewed the document for quality assurance and completeness. </li>
            <li> **Trigger Coverage**: Float value, ranging from 0 to 1. Cannot be below 0 or exceed 1. Represents the percentage of coverage for common software failure triggers that is completed in quality assurance process or testing. </li>
            <li> **SDLC Lifecycle Tabs**: [Mandatory] Names of the SDLC stages. Cannot be modified. Each tab represents a different lifecycle stage and must be filled out. For processes that have not completed all stages, leave blank any stages not yet accomplished. </li>
        </ul>
    Under Defect Data, the Excel file should contain:
        <ol>
            <li> **Under ODC tab**: Meta-data, not currently user modifiable. Will be modifiable in future expansions.</li>
            <li> **Under UCA Correlation tab**: This is the correlation data used to calculate failure probabilities between defects in the code and the likely failure mode triggered. Each value has a mean and sigma deviation value. The sum of row means must be equal to One (e.g., 100%). There are no other constraints on values. </li>
            <li> **Under HEMD tab**:
                <ul>
                    <li> **mu**: Hyperparameter, estimated correction factor </li>
                    <li> **sigma**: Hyperparameter, estimated deviation for lognormal distribution </li>
                    <li> **mean**: Estimated mean for lognormal distribution </li>
                </ul></li>
            <li> **Under BNN tab**: Meta-data, not currently user modifiable. Will be modifiable in future expansions. </li>
        </ol>


    To begin, first download the templates provided below. Do not change the column names or tab names. When complete, upload the Excel file to the site for generation.
"""
# --- End Page Overview

#%% --- Function Blocks ---
# Function to initialize persistence of data
def CA_persistence():
    # Persistent page assets
    if "CA_input_method" not in st.session_state:
        st.session_state.CA_input_method = None

    if "CA_tasks" not in st.session_state:
        st.session_state.CA_tasks = None
        st.session_state.CA_tasks_file_data = None
        st.session_state.CA_tasks_file_name = None
        st.session_state.CA_tasks_file_type = None

    if "CA_defects" not in st.session_state:
        st.session_state.CA_defects = None
        st.session_state.CA_defects_file_data = None
        st.session_state.CA_defects_file_name = None
        st.session_state.CA_defects_file_type = None

    if "CA_num_samples" not in st.session_state:
        st.session_state.CA_num_samples = 10000

    if "CA_plot_failure" not in st.session_state:
        st.session_state.CA_plot_failure = False

    if "CA_value" not in st.session_state:
        st.session_state.CA_value = True

    if "CA_submitted" not in st.session_state:
        st.session_state.CA_submitted = False

# Enables download of templates
def download_template():
    # Task Data metadata
    columns = [
        "Task Number",
        "Human Error Mode",
        "Task Description",
        "Review Number",
        "Trigger Coverage"
    ]
    task_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    human_error_modes = [
        "D1",
        "D1OC",
        "D1OC",
        "D1OC",
        "D1OC",
        "D2",
        "D2C",
        "D1"
    ]
    task_descriptions = [
        "Define the project purpose",
        "Identify hazards and risks",
        "Identify codes and standards",
        "Create a software management plan*",
        "Create a software verification and validation plan*",
        "Create a software configuration management plan*",
        "Create a software development plan*",
        "Create a software safety plan*"
    ]
    review_numbers = [2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2]
    trigger_coverages = [1, 0.975, 0.999, 0.945, 0.952, 1, 0.975, 0.999]

    df_Task = pd.DataFrame({
        "Task Number": task_numbers,
        "Human Error Mode": human_error_modes,
        "Task Description": task_descriptions,
        "Review Number": review_numbers,
        "Trigger Coverage": trigger_coverages
    })

    # Defect Data metadata
    # Page 1
    columns_ODC = [
            "Stages", "Algorithm", "Assignment", "Checking", "Documentation",
            "Function", "Interface", "Relationship", "Timing", "Total"
    ]
    labels_ODC = [
            "Concept",
            "Requirement",
            "Design",
            "Implementation",
            "Testing",
            "Install and Maintenance"
    ]
    values_ODC = [
            [0, 0, 0, 1000, 0, 0, 0, 0, 1000],
            [56, 26, 26, 107, 90, 57, 0, 13, 375],
            [56, 26, 26, 107, 90, 57, 0, 13, 375],
            [1215, 153, 240, 58, 372, 221, 8, 25, 2292],
            [1277, 181, 269, 12, 245, 361, 91, 28, 2464],
            [1277, 181, 269, 12, 245, 361, 91, 28, 2464]
    ]

    # Page 2
    columns_UCA = [
            "Defect Class",
            "UCA-A Mean", "UCA-A Sigma",
            "UCA-B Mean", "UCA-B Sigma",
            "UCA-C Mean", "UCA-C Sigma",
            "UCA-D Mean", "UCA-D Sigma"
    ]
    labels_UCA = [
            "Algorithm",
            "Assignment",
            "Checking",
            "Documentation",
            "Function",
            "Interface",
            "Relationship",
            "Timing"
    ]
    values_UCA = [
            [0.217, 0.0255, 0.525, 0.034, 0.124, 0.022, 0.134, 0.0095],
            [0.288, 0.076, 0.667, 0.065, 0.045, 0.036, 0,     0],
            [0.219, 0.037, 0.539, 0.0575, 0.102, 0.036, 0.141, 0.0645],
            [0.25,  0.125, 0.25,  0.125,  0.25,  0.125, 0.25,  0.125],
            [0.25,  0.077, 0.518, 0.032,  0.157, 0.046, 0.074,  0.108],
            [0.262, 0.0325, 0.579, 0.043, 0.093, 0.0475, 0.065, 0.0195],
            [0.25,  0.125, 0.25,  0.125,  0.25,  0.125, 0.25,  0.125],
            [0.095, 0.167, 0.19,  0.1445, 0.524, 0.2115, 0.19,  0.1445]
    ]

    # Page 3
    columns_HEMD = ["key", "description", "mu", "sigma", "mean"]
    labels_HEMD = [
            "D1", "D2", "C", "O", "OC",
            "D1C", "D1O", "D1OC", "D2C", "D2O", "D2OC"
    ]
    descriptions_HEMD = [
            "Diagnosis error (Diagnosis-1)",
            "Simple diagnosis error (Diagnosis-2)",
            "Omission error2",
            "Commission error",
            "Omission and Commission errors",
            "Diagnosis-1 and Omission",
            "Diagnosis-1 and Commission",
            "Diagnosis-1, Omission and Commission",
            "Diagnosis-2 and Omission",
            "Diagnosis-2 and Commission",
            "Diagnosis-2, Omission and Commission"
    ]
    values_HEMD = [
            [-9.21034, 2.0676, 8.48E-04],
            [-11.5129, 2.0676, 8.48E-05],
            [-5.80914, 0.978382, 4.84E-03],
            [-5.80914, 0.978382, 4.84E-03],
            [-5.116, 0.978382, 9.68E-03],
            [-5.63215, 0.94217, 5.58E-03],
            [-5.63215, 0.94217, 5.58E-03],
            [-5.00712, 0.942896, 1.04E-02],
            [-5.77788, 0.960271, 4.91E-03],
            [-5.77788, 0.960271, 4.91E-03],
            [-5.09867, 0.966776, 9.74E-03]
    ]

    # Page 4
    columns_BNN = [
            "Defect Class",
            "Concept (CS)",
            "Requirement (RR)",
            "Design (DR)",
            "Implementation (IMP)",
            "Testing (TS)",
            "Install & Maintenance (InM)",
            "Total"
    ]
    labels_BNN = [
            "Algorithm (AL)",
            "Assignment (AS)",
            "Checking (CH)",
            "Documentation (DC)",
            "Function (FN)",
            "Interface (IN)",
            "Relationship (RL)",
            "Timing (TM)"
    ]
    values_BNN = [
            ["K",  "Ki", "S",  "AA", "II", "QQ", "YY"],
            ["L",  "Li", "T",  "BB", "JJ", "RR", "ZZ"],
            ["M",  "Mi", "U",  "CC", "KK", "SS", "ZA"],
            ["N",  "Ni", "V",  "DD", "LL", "TT", "ZB"],
            ["O",  "Oi", "W",  "EE", "MM", "UU", "ZC"],
            ["P",  "Pi", "X",  "FF", "NN", "VV", "ZD"],
            ["Q",  "Qi", "Y",  "GG", "OO", "WW", "ZE"],
            ["R",  "Ri", "Z",  "HH", "PP", "XX", "ZF"]
    ]

    df_Defect_p1 = pd.DataFrame(values_ODC, columns=columns_ODC[1:])
    df_Defect_p1.insert(0, "Stages", labels_ODC)

    df_Defect_p2 = pd.DataFrame(values_UCA, columns=columns_UCA[1:])
    df_Defect_p2.insert(0, "Defect Class", labels_UCA)

    df_Defect_p3 = pd.DataFrame(values_HEMD, columns=["mu", "sigma", "mean"])
    df_Defect_p3.insert(0, "description", descriptions_HEMD)
    df_Defect_p3.insert(0, "key", labels_HEMD)

    df_Defect_p4 = pd.DataFrame(values_BNN, columns=columns_BNN[1:])
    df_Defect_p4.insert(0, "Defect Class", labels_BNN)

    with st.expander("General Instructions"):
        st.markdown(general_instructions, unsafe_allow_html=True)
        st.text("Click below to download a template to input SDLC data.")

        # Setup for xlsx download of the Task data template
        output1 = BytesIO()
        with pd.ExcelWriter(output1, engine='xlsxwriter') as writer:
            df_Defect_p1.to_excel(writer, sheet_name="ODC", index=False)
            df_Defect_p2.to_excel(writer, sheet_name="UCA Correlation", index=False)
            df_Defect_p3.to_excel(writer, sheet_name="HEMD", index=False)
            df_Defect_p4.to_excel(writer, sheet_name="BNN", index=False)

        defect_xlsx_data = output1.getvalue()

        st.download_button(
            label="⬇️ Download Template_Defect_Data.xlsx",
            data=defect_xlsx_data,
            file_name="Template_Defect_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Setup for xlsx download of the Task data template
        output2 = BytesIO()
        with pd.ExcelWriter(output2, engine='xlsxwriter') as writer:
            df_Task.to_excel(writer, sheet_name="Concept", index=False)
            df_Task.to_excel(writer, sheet_name="Requirement", index=False)
            df_Task.to_excel(writer, sheet_name="Design", index=False)
            df_Task.to_excel(writer, sheet_name="Implementation", index=False)
            df_Task.to_excel(writer, sheet_name="Testing", index=False)
            df_Task.to_excel(writer, sheet_name="Install and Maintenance", index=False)

        task_xlsx_data = output2.getvalue()

        st.download_button(
            label="⬇️ Download Template_Task_Data.xlsx",
            data=task_xlsx_data,
            file_name="Template_Task_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    return

# Function to reset submission button status when a change is made in the input
def reset_submission():
    st.session_state.CA_submitted = False

# Function to run and plot the output
def runAndPlot(software_BBN):
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
    if st.session_state.CA_plot_failure:
        fig = software_BBN.plot(save=False, show=False)
        if isinstance(fig, list):
            for f in fig:
                st.plotly_chart(f)

@st.dialog("Input Error")
def error_InputError():
    st.write("The input file chosen is incorrect. Please try again.")

# Function to show previously loaded files for tasks
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
                {st.session_state.CA_tasks_file_name}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.button("✖", key="clear_task_btn", on_click=clear_task)

# Function to clear previous uploaded file if user clicks on the X
def clear_task():
    st.session_state.CA_tasks = None

# Function to show previously loaded files for defect
def defect_box():
    col1, col2 = st.columns([8, 1])

    with col1:
        st.write(
            f"""
            <div style="padding:10px;
                        border:1px solid #ccc;
                        border-radius:5px;
                        background-color:#f7f7f7;
                        font-weight:600;">
                {st.session_state.CA_defects_file_name}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.button("✖", key="clear_defect_btn", on_click=clear_defect)

# Function to clear previous uploaded file if user clicks on the X
def clear_defect():
    st.session_state.CA_defects = None

# Main App Page
def app():
    # Initialize persistent data storage
    CA_persistence()

    # Begin header
    st.markdown(page_title, unsafe_allow_html=True)

    download_template()

    # Uploaded Tasks
    CAtasks = st.file_uploader('Upload task data', type=['xlsx'], key="CA_uploader", on_change=reset_submission)
    if st.session_state.CA_tasks != None and CAtasks == None:
        # Show last uploaded file with option to remove
        st.session_state.CA_tasks_file_data = st.session_state.CA_tasks.read()
        st.session_state.CA_tasks_file_name = st.session_state.CA_tasks.name
        st.session_state.CA_tasks_file_type = st.session_state.CA_tasks.type
        task_box()
    else:
        # Overwrite stored information
        st.session_state.CA_tasks = CAtasks

    # Uploaded Defects
    CAdefects = st.file_uploader('Upload defect data (optional)', type=['xlsx'], key="CA_defect_uploader", on_change=reset_submission)
    if st.session_state.CA_defects != None and CAdefects == None:
        # Show last uploaded file with option to remove
        st.session_state.CA_defects_file_data = st.session_state.CA_defects.read()
        st.session_state.CA_defects_file_name = st.session_state.CA_defects.name
        st.session_state.CA_defects_file_type = st.session_state.CA_defects.type
        defect_box()
    else:
        # Overwrite stored information
        st.session_state.CA_defects = CAdefects

    # Number of samples w/ persistence
    st.session_state.CA_num_samples = st.number_input("Number of samples", min_value=1, max_value=99999, value=st.session_state.CA_num_samples, key="CA_num", on_change=reset_submission)

    # Plot option checkbox w/ persistence
    st.session_state.CA_plot_failure = st.checkbox('Visualize', value=st.session_state.CA_plot_failure, key="CA_plot", on_change=reset_submission)

    with st.form("CA_user_form"):
        try:
            submitted = st.form_submit_button("Calculate", type="primary", width="stretch")
            if submitted == True:
                st.session_state.CA_submitted = submitted
        except:
            submitted = st.form_submit_button("Calculate", type="primary", use_container_width=True)
            if submitted == True:
                st.session_state.CA_submitted = submitted

    if st.session_state.CA_submitted:
        if st.session_state.CA_tasks == None:
            error_InputError()
        else:
            if st.session_state.CA_defects is not None:
                software_BBN = BBN(st.session_state.CA_defects, st.session_state.CA_tasks, st.session_state.CA_num_samples)
            else:
                software_BBN = BBN(defect_data, st.session_state.CA_tasks, st.session_state.CA_num_samples)

            runAndPlot(software_BBN)

    else:
        pass
