# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
import pandas as pd
import io
import os, sys

# Bahamas Module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from bahamas.cccg import CCCG

workdir = os.path.dirname(__file__)
sys_data = os.path.join(workdir, '..', '..', 'data', 'Scenario_6.csv')


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
def load_file():
    """
    Enables users to load a csv file to compute. 
    """
    with st.container(border=False):
        with st.form("opener"):
            sys_data = st.file_uploader('Upload your data', type=['csv'])
            submitted = st.form_submit_button("Generate", 
                                              type="primary",
                                              use_container_width=True)
    return submitted, sys_data

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

def configuration_options():
    with st.form("Options"):
        all_groups = st.checkbox('All', value=True)
        single     = st.checkbox('Single')
        double     = st.checkbox('Double')
        triple     = st.checkbox('Triple')
                
        config = {'output_file_base': None,
                  'final':all_groups,
                  'single':single,
                  'double':double,
                  'triple':triple}
    
    return config

def show_CCCG(expanded, sys_data):
    cccg_obj = CCCG(file=sys_data)
    cccg_obj.generate()
    
    opts = ['Summary Statistics', 'All Groups', 'Single Factor', 'Double Factor', 'Triple Factors']
    opt_index = list(range(len(opts)))
    opt_dict  = dict(zip(opts, opt_index))
    
    tabs = st.tabs(opts)
    
    with tabs[opt_dict["Summary Statistics"]]:
        final  = cccg_obj.get('final')
        single = cccg_obj.get('single')
        double = cccg_obj.get('double')
        triple = cccg_obj.get('triple') 
        
        total_cnt    = len(final)
        total_single = len(single)
        total_double = len(double)
        total_triple = len(triple)
        
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
        final = cccg_obj.get('final')
        st.subheader("All CCCGs based on different combination of coupling factors (i.e., Function, Input and Design)")
        for i, df in enumerate(final):
            label = f"CCCG {i+1}"
            with st.expander(label=label, expanded=expanded):
                st.dataframe(df)

    with tabs[opt_dict['Single Factor']]: 
        single = cccg_obj.get('single')
        st.subheader("CCCGs Based on Single Coupling Factor")
        for i, df in enumerate(single):
            label = f"CCCG {i+1}"
            with st.expander(label=label, expanded=expanded):
                st.dataframe(df)
          
    with tabs[opt_dict['Double Factor']]:
        double = cccg_obj.get('double')
        st.subheader("CCCGs Based on Two Coupling Factors")
        for i, df in enumerate(double):
            label = f"CCCG {i+1}"
            with st.expander(label=label, expanded=expanded):
                st.dataframe(df)
          
    with tabs[opt_dict['Triple Factors']]:
        triple = cccg_obj.get('triple')
        st.subheader("CCCG Based on Three Coupling Factors")
        for i, df in enumerate(triple):
            label = f"CCCG {i+1}"
            with st.expander(label=label, expanded=expanded):
                st.dataframe(df)
    
#%% --- Main Page Information    
def app():
    # st.set_page_config(page_title="Software Common Cause Analysis",
    #                 page_icon=":bridge_at_night:",
    #                 layout="wide",
    #                 initial_sidebar_state="auto")
    
    
    st.markdown(page_title,unsafe_allow_html=True,)
    
    download_template()
    
    submitted, sys_data = load_file()
    
    with st.container(border=True):
        expanded     = st.checkbox('Expand All Results?')
    
    if submitted:
        show_CCCG(expanded, sys_data)
        
