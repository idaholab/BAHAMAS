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

# Functions for configure
def configure_sidebar() -> None:
    """
    Setup and display the sidebar elements.

    This function configures the sidebar of the Streamlit application,
    including the form for user inputs and the resources section.
    """
    with st.sidebar:
        with st.form("my_form"):
            st.info("**CCCGs Generation! Start here ↓**", icon="👋🏾")
            sys_data = st.file_uploader('Upload your data', type=['csv'])
            st.markdown('**CCCG Output Options**')
            file_base = st.text_input('File Base', 'cccg', key='file_base')
            final = st.checkbox('All', value=True)
            single = st.checkbox('Single')
            double = st.checkbox('Double')
            triple = st.checkbox('Triple')
            config = {'output_file_base': file_base,
                      'final':final,
                      'single':single,
                      'double':double,
                      'triple':triple}

            # The Big Red "Submit" Button!
            submitted = st.form_submit_button(
                "Generate", type="primary", use_container_width=True)
        return submitted, sys_data,config


def app():
    submitted, sys_data, config = configure_sidebar()
    st.set_page_config(page_title="Software Common Cause Analysis",
                    page_icon=":bridge_at_night:",
                    layout="wide",
                    initial_sidebar_state="auto")

    st.header("""Software Common Cause Analysis""")
    if submitted:
        cccg_obj = CCCG(file=sys_data)
        cccg_obj.generate(config=config)

        opts = []
        tabInfo = {}
        i = 0
        for opt in ['final', 'single', 'double', 'triple']:
          if config[opt]:
            opts.append("✅ CCCGs " + opt)
            tabInfo[opt] = i
            i += 1

        tabs = st.tabs(opts)

        if config['final']:
          final = cccg_obj.get('final')
          with tabs[tabInfo['final']]:
            st.subheader("All CCCGs based on different combination of coupling factors (i.e., Function, Input and Design)")
            for i, df in enumerate(final):
              st.title(f'CCCG {i+1}')
              st.dataframe(df)

        if config['single']:
          single = cccg_obj.get('single')
          with tabs[tabInfo['single']]:
            st.subheader("CCCGs based on single coupling factor (i.e., Function or Input or Design)")
            for i, df in enumerate(single):
              st.title(f'CCCG {i+1}')
              st.dataframe(df)
        if config['double']:
          double = cccg_obj.get('double')
          with tabs[tabInfo['double']]:
            st.subheader("CCCGs based on two coupling factors (i.e., Function and Input, Function and Design or Input and Design)")
            for i, df in enumerate(double):
              st.title(f'CCCG {i+1}')
              st.dataframe(df)
        if config['triple']:
          triple = cccg_obj.get('triple')
          with tabs[tabInfo['triple']]:
            st.subheader("CCCG based on three coupling factors (i.e., Function, Input and Design)")
            for i, df in enumerate(triple):
              st.title(f'CCCG {i+1}')
              st.dataframe(df)

