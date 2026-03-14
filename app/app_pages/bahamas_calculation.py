# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
import pandas as pd
import os, sys

# Bahamas Module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from bahamas.utils import  UCA_types
from bahamas.software_total_failure_probability_bbn import BBN

# streamlit and extra
# container always at the bottom
from streamlit_extras.bottom_container import bottom

# Data:

workdir = os.path.dirname(__file__)
defect_data = os.path.join(workdir, '..', '..', 'data', 'Defect_Data.xlsx')

# Functions for configure
def configure_inputs() -> None:
    """
    Setup and display the main-page input controls.

    This function renders the data upload and calculation controls
    directly in the main page content area.
    """
    with st.container(border=True):
        st.caption("Upload the required files and configure the calculation before running the model.")
        with st.form("my_form"):
            defects = None
            mode = None
            tasks = st.file_uploader('Upload your data', type=['xlsx'])
            defects = st.file_uploader('Upload defect data (optional)', type=['xlsx'])
            # mode = st.selectbox("Calculation mode", ('Stochastic', 'Deterministic'))
            num_samples = st.number_input("Number of samples", value=10000)
            plot_failure = st.checkbox('visualize')
            submitted = st.form_submit_button(
                "Calculate", type="primary", use_container_width=True)
    return submitted, mode, num_samples, plot_failure, tasks, defects


def app():
    st.markdown(
        """
        <h2 style="white-space: nowrap; text-align: center; color: #16324f;">
            Comprehensive Assessment
        </h2>
        """,
        unsafe_allow_html=True,
    )
    submitted, mode, num_samples, plot_failure, tasks, defects = configure_inputs()

    # st.set_page_config(page_title="BAHAMAS",
    #                 # page_icon=":bridge_at_night:",
    #                 page_icon="../docs/pics/bahamas_structure.png",
    #                 layout="wide",
    #                 initial_sidebar_state="auto")
    # st.logo("./docs/pics/bahamas_structure.png")
    # st.image("../docs/pics/bahamas_structure.png", width=200)

    if submitted:
        output = {}
        style = {}
        if defects is not None:
            software_BBN = BBN(defects, tasks, num_samples)
        else:
            software_BBN = BBN(defect_data, tasks, num_samples)
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
