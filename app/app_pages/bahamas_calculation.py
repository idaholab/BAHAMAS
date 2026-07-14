# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

# built-in libraries
import os, sys
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
defect_data = os.path.join(workdir, '..', '..', 'data', 'Defect_Data.xlsx')

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
    st.markdown(
        """
        <h2 style="white-space: nowrap; text-align: center; color: #16324f;">
            Comprehensive Assessment
        </h2>
        """,
        unsafe_allow_html=True,
    )
    
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
