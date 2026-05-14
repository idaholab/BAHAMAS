# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

# built-in libraries
import os, sys
import io
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# implicit libraries
import streamlit as st
import pandas as pd

# explicit libraries
from bahamas.cccg import CCCG
workdir = os.path.dirname(__file__)        

#%% --- Page Overview Text Descriptions ---
page_overview = "Upload the system data and select the common cause component group (CCCG) output options to generate."
page_title = """
    <h2 style="white-space: nowrap; text-align: center; color: #16324f;">
    Common Cause Component Group Identification 
    </h2>
"""

general_instructions = """
    This page enables common cause failure groups to be identified from a list of components. In summary, the user generates a list of all components. For each component, the user will identify a coupling factor. 
    A coupling factor in this application is one of the following:
        - Functional factor: What is the function of the component?
        - Design factor: What is the design of the component?
        - Input factor: What are the inputs to this component?
    Notice that each factor does not inherently consider whether components are coupled together. Each factor is a general description of the component. When the algorithm is RUN, it will determine, among entered factors, which can be grouped together. 

    To begin, first download the template provided below. Do not change the column names. For each component (whether redundant or unique) enter a new line and the associated factors. When complete, upload the csv file to the site for generation.
"""

# --- End Page Overview 

#%% --- Tab All CCCG Text ---

# --- End Tab ---

#%% --- Tab Single CCCG Text ---

# --- End Tab ---

#%% --- Tab Double CCCG Text ---

# --- End Tab ---

#%% --- Tab Triple CCCG Text

# --- End Tab ---

#%% --- Function Blocks ---
# Function to initialize persistence of data
def CCI_persistence():
    # Persistent page assets        
    if "CCI_tasks" not in st.session_state:
        st.session_state.CCI_tasks = None
        st.session_state.CCI_uploaded_file_data = None
        st.session_state.CCI_uploaded_file_name = None
        st.session_state.CCI_uploaded_file_type = None
        
    if "CCI_submitted" not in st.session_state:
        st.session_state.CCI_submitted = False
        
    if "CCI_expand" not in st.session_state:
        st.session_state.CCI_expand = False
    
    if "CCI_CCCG" not in st.session_state:
        st.session_state.CCI_CCCG        = False
        st.session_state.CCI_final       = None
        st.session_state.CCI_single      = None
        st.session_state.CCI_double      = None
        st.session_state.CCI_triple      = None
        st.session_state.skip_generation = True
        

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
                {st.session_state.CCI_uploaded_file_name}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.button("✖", key="clear_title_btn", on_click=clear_task)

# Function to reset submission button status when a change is made in the input
def reset_submission():
    st.session_state.CCI_submitted = False
    
# Function to clear previous uploaded file if user clicks on the X
def clear_task():
    st.session_state.CCI_tasks = None
    st.session_state.submitted = False

@st.dialog("Input Error")
def error_InputError():
    st.write("The input file chosen is incorrect. Please try again.")
    
def update_generation():
    st.session_state.skip_generation = False
    
def download_template():
    with st.expander("General Instructions"):
        st.text(general_instructions)
        st.text("Click below to download a template to input CCCG data.")
        
        df = pd.DataFrame(
            [
                {
                    "Component_Name": "PSensor_Div1",
                    "Division": "1",
                    "Function_Config": "Pressure sensor",
                    "Input_Config": "Pressure (psig) from reactor",
                    "Design_Config": "Bourdon pressure sensor",
                },
                {
                    "Component_Name": "PSensor_Div2",
                    "Division": "2",
                    "Function_Config": "Pressure sensor",
                    "Input_Config": "Pressure (psig) from reactor",
                    "Design_Config": "Bourdon pressure sensor",
                }
            ]
        )
        
        csv_data = df.to_csv(index=False)
        
        st.download_button(
            label="⬇️ Download Template.csv",
            data=csv_data,
            file_name="Template.csv",
            mime="text/csv"
            )

    return 

def show_CCCG(expanded, sys_data, skip_generate):
    
    if not skip_generate:    
        cccg_obj = CCCG(file=sys_data)
        cccg_obj.generate()
        st.session_state.CCI_final  = cccg_obj.get('final')
        st.session_state.CCI_single = cccg_obj.get('single')
        st.session_state.CCI_double = cccg_obj.get('double')
        st.session_state.CCI_triple = cccg_obj.get('triple')
        st.session_state.skip_generation = True
    
    opts = ['Summary Statistics', 'All Groups', 'Single Factor', 'Double Factor', 'Triple Factors']
    opt_index = list(range(len(opts)))
    opt_dict  = dict(zip(opts, opt_index))
    
    tabs = st.tabs(opts)
    
    final  = st.session_state.CCI_final
    single = st.session_state.CCI_single
    double = st.session_state.CCI_double
    triple = st.session_state.CCI_triple
    
    plot_statistics(tabs, opt_dict, final, single, double, triple, expanded)
    
    return tabs, opt_dict, final, single, double, triple
    
def plot_statistics(tabs, opt_dict, final, single, double, triple, expanded):
    
    with tabs[opt_dict["Summary Statistics"]]:
        df = pd.concat(final)
        
        # Show frequency of components in CCCG
        with st.expander("Frequency of Components in CCCG", expanded=expanded):
            st.text("Frequency a component appearance in CCCGs.")
            freq_df = (
                df["Component_Name"]
                .value_counts(dropna=False)       # set dropna=True if you don't want NaNs counted
                .reset_index(name="frequency")
                .rename(columns={"Component_Name": "Component Name", "frequency": "Component Freq. in CCCG"})
                .sort_values("Component Freq. in CCCG", ascending=True)
            )
            
            st.dataframe(freq_df, hide_index=True)
        
        # Show frequency of function coupling factors in CCCG
        with st.expander("Frequency of Function Coupling Factor in CCCG", expanded=expanded):
            st.text("Frequency of coupling factor appearance in CCCGs.")
            
            factor_df = df["Function_Config"].str.split(";").explode()
            
            factor_df = (
                        factor_df
                        .value_counts(dropna=True)
                        .reset_index(name="frequency")
                        .rename(columns={"Function_Config": "Function Coupling Factor", "frequency": "Factor Freq. in CCCG"})
                        .sort_values("Factor Freq. in CCCG", ascending=True)
            )
            st.dataframe(factor_df, hide_index=True)

        # Show frequency of design coupling factors in CCCG. 
        with st.expander("Frequency of Design Coupling Factor in CCCG", expanded=expanded):
            st.text("Frequency of Design coupling factor appearance in CCCGs.")
            
            factor_df = df["Design_Config"].str.split(";").explode()
            
            factor_df = (
                        factor_df
                        .value_counts(dropna=True)
                        .reset_index(name="frequency")
                        .rename(columns={"Design_Config": "Design Coupling Factor", "frequency": "Factor Freq. in CCCG"})
                        .sort_values("Factor Freq. in CCCG", ascending=True)
            )
            st.dataframe(factor_df, hide_index=True)   
            
        # Show frequency of input coupling factors in CCCG. 
        with st.expander("Frequency of Input Coupling Factor in CCCG", expanded=expanded):
            st.text("Frequency of Input coupling factor appearance in CCCGs.")
            
            factor_df = df["Input_Config"].str.split(";").explode()
            
            factor_df = (
                        factor_df
                        .value_counts(dropna=True)
                        .reset_index(name="frequency")
                        .rename(columns={"Input_Config": "Input Coupling Factor", "frequency": "Factor Freq. in CCCG"})
                        .sort_values("Factor Freq. in CCCG", ascending=True)
            )
            st.dataframe(factor_df, hide_index=True)            
        
    with tabs[opt_dict['All Groups']]:
        st.subheader("All CCCGs based on different combination of coupling factors (i.e., Function, Input and Design)")
        for i, df in enumerate(final):
            label = f"CCCG {i+1}"
            with st.expander(label=label, expanded=expanded):
                st.dataframe(df)

    with tabs[opt_dict['Single Factor']]: 
        st.subheader("CCCGs Based on Single Coupling Factor")
        for i, df in enumerate(single):
            label = f"CCCG {i+1}"
            with st.expander(label=label, expanded=expanded):
                st.dataframe(df)
          
    with tabs[opt_dict['Double Factor']]:
        st.subheader("CCCGs Based on Two Coupling Factors")
        for i, df in enumerate(double):
            label = f"CCCG {i+1}"
            with st.expander(label=label, expanded=expanded):
                st.dataframe(df)
          
    with tabs[opt_dict['Triple Factors']]:
        st.subheader("CCCG Based on Three Coupling Factors")
        for i, df in enumerate(triple):
            label = f"CCCG {i+1}"
            with st.expander(label=label, expanded=expanded):
                st.dataframe(df)
    
#%% --- Main Page Information    
def app():
    CCI_persistence()    
    
    st.markdown(page_title,unsafe_allow_html=True,)
    
    download_template()

    #uploaded = st.file_uploader('Upload your data', type=['csv'], key="CCI_uploader")
    uploaded = st.file_uploader('Upload your data', type=['xlsx'], key="CCI_uploader")    
    
    if st.session_state.CCI_tasks != None and uploaded == None:
        # Show last uploaded file with option to remove
        st.session_state.CCI_uploaded_file_data = st.session_state.CCI_tasks.read()
        st.session_state.CCI_uploaded_file_name = st.session_state.CCI_tasks.name
        st.session_state.CCI_uploaded_file_type = st.session_state.CCI_tasks.type
        task_box()
    else:
        # Overwrite stored information
        st.session_state.CCI_tasks = uploaded
    
    with st.form("CCI_opener"):             
        try:
            submitted = st.form_submit_button("Generate", type="primary", width="stretch", on_click=update_generation)
        except:
            submitted = st.form_submit_button("Generate", type="primary", use_container_width=True, on_click=update_generation)
                
        if submitted == True:
            st.session_state.CCI_submitted = submitted
            
    with st.container(border=True):
        st.session_state.CCI_expand     = st.checkbox('Expand All Results?', value=st.session_state.CCI_expand)
    
    
    if st.session_state.CCI_submitted and st.session_state.CCI_tasks is not None:
        show_CCCG(st.session_state.CCI_expand, st.session_state.CCI_tasks, st.session_state.skip_generation)
