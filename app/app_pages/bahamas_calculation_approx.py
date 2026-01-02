# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
import pandas as pd
import os, sys

# Bahamas Module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from bahamas.utils import SDLC_stages, UCA_types
from bahamas.software_total_failure_probability_bbn import BBN


# streamlit and extra

# container always at the bottom
from streamlit_extras.bottom_container import bottom

# Data:

workdir = os.path.dirname(__file__)
defect_data = os.path.join(workdir, '..', '..', 'data', 'Defect_Data.xlsx')

# Functions for configure
def configure_sidebar() -> None:
    """
    Setup and display the sidebar elements.

    This function configures the sidebar of the Streamlit application,
    including the form for user inputs and the resources section.
    """
    with st.sidebar:
        with st.form("my_form"):
            st.info("**Assessment! Start here ↓**", icon="👋🏾")
            # with st.expander(":orange[**Refine Calculation**]"):
            # Advanced Settings (for the curious minds!)
            defects = None
            tasks = st.file_uploader('Upload your data', type=['xlsx'])
            defects = st.file_uploader('Upload defect data (optional)', type=['xlsx'])
            mode = st.selectbox("Calculation mode", ('Stochastic', 'Deterministic'))
            num_samples = st.number_input("Number of samples", value=10000)
            plot_failure = st.checkbox('visualize')

            # The Big Red "Submit" Button!
            submitted = st.form_submit_button(
                "Calculate", type="primary", use_container_width=True)
        return submitted, mode, num_samples, plot_failure, tasks, defects


def app():
    # st.set_page_config(page_title="BAHAMAS",
    #                 # page_icon=":bridge_at_night:",
    #                 page_icon="../docs/pics/bahamas_structure.png",
    #                 layout="wide",
    #                 initial_sidebar_state="auto")
    # st.logo("./docs/pics/bahamas_structure.png")
    # st.image("../docs/pics/bahamas_structure.png", width=200)

    st.header("""BAHAMAS: Software Reliability Assessment""")

    user_inputs = {}
    tasks = None
    input_method = st.selectbox("Choose input method:", ("Choose...","Upload Data", "Type in Data"))
    if input_method == "Upload Data":
        tasks = st.file_uploader('Upload your data', type=['xlsx'])
    elif input_method == "Type in Data":
        for i in range(0,6):
            st.subheader(f'{SDLC_stages[i]}:')
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                mean = st.number_input('Human Error Probability (Mean)', value=0.25, step=0.0001, key=f"mean_{i}")
            with col2:
                std = st.number_input('Human Error Probability (STD)', value=0.05, step=0.0001, key=f"std_{i}")
            with col3:
                review_number = st.number_input('Review Number', value=2.15, step=0.01, key=f"review_{i}")
            with col4:
                trigger_coverage = st.number_input('Trigger Coverage', value=0.9, step=0.01, key=f"trigger_{i}")
            user_inputs[SDLC_stages[i]] = {'mean':mean, 'std':std, 'review':review_number, 'trigger':trigger_coverage}
    num_samples = st.number_input("Number of samples", value=10000)
    plot_failure = st.checkbox('visualize')

    with st.form("user_form"):
        # The Big Red "Submit" Button!
        submitted = st.form_submit_button(
            "Calculate", type="primary", use_container_width=True)


    if submitted:
        output = {}
        style = {}
        if input_method == "Upload Data":
            software_BBN = BBN(defect_data, tasks, num_samples=num_samples, approx=True)
        else:
            software_BBN = BBN(defect_data, tasks, data=user_inputs, num_samples=num_samples, approx=True)
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
        st.subheader("""Calculation Results""")
        st.info("**Assessment Result ↓**", icon="👋🏾")

        st.dataframe(styled_df)
        # visualize data
        if plot_failure:
            fig = software_BBN.plot(save=False, show=False)
            if isinstance(fig, list):
                for f in fig:
                    st.plotly_chart(f)
    else:
        pass



    with bottom():
        st.markdown("#### Bayesian and Human Reliability Analysis-Aided Method for the Reliability Analysis of Software (BAHAMAS)")
        st.markdown('''For help or feedback, contact congjian.wang@inl.gov.
                For more options and information, check out the
                [GitHub repository](https://github.inl.gov/congjian-wang/BAHAMAS) or
                [Report](https://lwrs.inl.gov/content/uploads/11/2024/11/2448420.pdf)
                ''')

