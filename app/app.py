# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
import logging
import os
from streamlit_option_menu import option_menu

from app_pages import bahamas_calculation
from app_pages import bahamas_calculation_approx
from app_pages import cccg_generation
from app_pages import Software_Quality_Survey, Analysis
from app_pages import cccg_survey
from app_pages import welcome

logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="Digital I&C Risk Assessment Platform",
    page_icon="🌟",
    layout="centered",
    initial_sidebar_state="expanded"
)

if __name__ == "__main__":

    # Initialize session state if not already done
    if 'shared_data' not in st.session_state:
        st.session_state['shared_data'] = ''

    # Create a sidebar menu for navigation
    with st.sidebar:
        selected_page = option_menu(
            "BAHAMAS",
            ["Welcome","Preliminary Assessment", "Comprehensive  Assessment", "Common Cause Analysis", "Software Quality Survey", "CCCG Evaluation"],
            icons=["house", "rocket","fire", "pen", "pen", "gear"],
            menu_icon="cast",
            default_index=0,
        )

    # Display the selected page
    if selected_page == "Welcome":
        welcome.app()
    elif selected_page == "Comprehensive  Assessment":
        bahamas_calculation.app()
    elif selected_page == "Preliminary Assessment":
        bahamas_calculation_approx.app()
    elif selected_page == "Common Cause Analysis":
        cccg_generation.app()
    elif selected_page == "Software Quality Survey":
        Software_Quality_Survey.app()
    elif selected_page == "CCCG Evaluation":
        cccg_survey.app()




