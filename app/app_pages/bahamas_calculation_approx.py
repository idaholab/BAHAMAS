# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

# built-in libraries
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# implicit libraries
import streamlit as st
from streamlit_extras.bottom_container import bottom
import pandas as pd

# explicit libraries
from bahamas.utils import SDLC_stages, UCA_types
from bahamas.software_total_failure_probability_bbn import BBN

# Reference data location for defect correlations
workdir = os.path.dirname(__file__)
defect_data = os.path.join(workdir, '..', '..', 'data', 'Defect_Data.xlsx')

# Function to initialize persistence of data
def PA_persistence():
    # Persistent page assets 
    if "PA_input_method" not in st.session_state:
        st.session_state.PA_input_method = None
        
    if "PA_tasks" not in st.session_state:
        st.session_state.PA_tasks = None
        st.session_state.PA_uploaded_file_data = None
        st.session_state.PA_uploaded_file_name = None
        st.session_state.PA_uploaded_file_type = None
        
    if "PA_num_samples" not in st.session_state:
        st.session_state.PA_num_samples = 10000
        
    if "PA_plot_failure" not in st.session_state:
        st.session_state.PA_plot_failure = False
        
    if "PA_value" not in st.session_state:
        st.session_state.PA_value = True
        
    if "PA_submitted" not in st.session_state:
        st.session_state.PA_submitted = False
        
    if "PA_user_inputs" not in st.session_state:
        st.session_state.PA_user_inputs = {}

# Function to initialize persistence of table data
def PA_persistence_value(rewrite):
    if rewrite:
        st.write("Here")
        # Ensure persistent values exist for all 6 stages & values
        for i in range(6):
            if f"mean_{i}" not in st.session_state:
                st.session_state[f"mean_{i}"]    = 0.25
            if f"std_{i}" not in st.session_state:
                st.session_state[f"std_{i}"]     = 0.05
            if f"review_{i}" not in st.session_state:
                st.session_state[f"review_{i}"]  = 2.15
            if f"trigger_{i}" not in st.session_state:
                st.session_state[f"trigger_{i}"] = 0.90
    else: return

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
                {st.session_state.PA_uploaded_file_name}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.button("✖", key="clear_title_btn", on_click=clear_task)
    
# Function to clear previous uploaded file if user clicks on the X
def clear_task():
    st.session_state.PA_tasks = None
    
# Function to reset submission button status when a change is made in the input
def reset_submission():
    st.session_state.PA_submitted = False

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
    # visualize data
    if st.session_state.PA_plot_failure:
        fig = software_BBN.plot(save=False, show=False)
        if isinstance(fig, list):
            for f in fig:
                st.plotly_chart(f)    
                
@st.dialog("Input Error")
def error_InputError():
    st.write("The input file chosen is incorrect. Please try again.")

@st.dialog("No Chosen Input Method")
def error_NoMethod():
    st.write("The method for calculation is not selected.")
    
# Main App Page
def app():
    # Initialize persistent data storage
    PA_persistence()
    PA_persistence_value(st.session_state.PA_value)
    st.session_state.PA_value = False
    
    # Begin header
    st.markdown(
        """
        <h2 style="white-space: nowrap; text-align: center; color: #16324f;">
            Preliminary Assessment
        </h2>
        """,
        unsafe_allow_html=True,
    )
    
    # Input choice 
    options = ["Choose...", "Upload Data", "Type in Data"]
    if st.session_state.PA_input_method == None:
        st.session_state.PA_input_method = st.selectbox("Choose input method:", options, on_change=reset_submission)
    else:
        st.session_state.PA_input_method = st.selectbox("Choose input method:", options, index=options.index(st.session_state.PA_input_method), on_change=reset_submission)
        
    # Upload data 
    if st.session_state.PA_input_method == "Upload Data":
        
        uploaded = st.file_uploader('Upload your data', type=['xlsx'], key="PA_uploader")
        
        if st.session_state.PA_tasks != None and uploaded == None:
            # Show last uploaded file with option to remove
            st.session_state.PA_uploaded_file_data = st.session_state.PA_tasks.read()
            st.session_state.PA_uploaded_file_name = st.session_state.PA_tasks.name
            st.session_state.PA_uploaded_file_type = st.session_state.PA_tasks.type
            task_box()
        else:
            # Overwrite stored information
            st.session_state.PA_tasks = uploaded

    elif st.session_state.PA_input_method == "Type in Data":
        for i in range(0,6):
            st.subheader(f'{SDLC_stages[i]}:')
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.session_state[f"mean_{i}"]      = st.number_input('Human Error Prob. (Mean)', min_value=0.0, max_value=1.0, value=st.session_state[f"mean_{i}"],    step=0.01, key=f"MN_{i}", on_change=reset_submission)
            with col2:
                st.session_state[f"std_{i}"]       = st.number_input('Human Error Prob. (STD)',  min_value=0.0, max_value=99.0, value=st.session_state[f"std_{i}"],     step=0.01, key=f"SD_{i}", on_change=reset_submission)
            with col3:
                st.session_state[f"review_{i}"]    = st.number_input('Review Number',            min_value=0.0, max_value=6.0, value=st.session_state[f"review_{i}"],  step=1.0,   key=f"RV_{i}", on_change=reset_submission)
            with col4:
                st.session_state[f"trigger_{i}"]   = st.number_input('Trigger Coverage',         min_value=0.0, max_value=1.0, value=st.session_state[f"trigger_{i}"], step=0.1,   key=f"TG_{i}", on_change=reset_submission)
                
            st.session_state.PA_user_inputs[SDLC_stages[i]] = {'mean':st.session_state[f"mean_{i}"], 'std':st.session_state[f"std_{i}"], 'review':st.session_state[f"review_{i}"], 'trigger':st.session_state[f"trigger_{i}"]}
    
    # Number of samples w/ persistence
    st.session_state.PA_num_samples = st.number_input("Number of samples", min_value=1, max_value=99999, value=st.session_state.PA_num_samples, key="PA_num", on_change=reset_submission)
    
    # Plot option checkbox w/ persistence
    st.session_state.PA_plot_failure = st.checkbox('visualize', value=st.session_state.PA_plot_failure, key="PA_plot", on_change=reset_submission)

    with st.form("PA_user_form"):
        # The Big Red "Submit" Button!
        try:
            submitted = st.form_submit_button("Calculate", type="primary", width="stretch")
            if submitted == True:
                st.session_state.PA_submitted = submitted
        except:
            submitted = st.form_submit_button("Calculate", type="primary", use_container_width=True)
            if submitted == True:
                st.session_state.PA_submitted = submitted
        
    if st.session_state.PA_submitted:        
        if st.session_state.PA_input_method == "Upload Data":
            if st.session_state.PA_tasks == None:
                error_InputError()
            else:
                software_BBN = BBN(defect_data, st.session_state.PA_tasks, num_samples=st.session_state.PA_num_samples, approx=True)
                runAndPlot(software_BBN)
        elif st.session_state.PA_input_method == "Type in Data":
            software_BBN = BBN(defect_data, st.session_state.PA_tasks, data=st.session_state.PA_user_inputs, num_samples=st.session_state.PA_num_samples, approx=True)
            runAndPlot(software_BBN)
        else:
            error_NoMethod()
    else:
        pass



