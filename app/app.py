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

logo_path = "../docs/pics/BAHAMAS_color.png"

# Set page configuration
st.set_page_config(
    page_title="Digital I&C Risk Assessment Platform",
    page_icon="🌟",
    layout="centered",
    initial_sidebar_state="expanded"
)

def display_logo(logo_path: str):
    """Displays the logo in the sidebar or a placeholder if the logo is not found.

    Args:
        logo_path (str): The file path for the logo image.
    """
    if os.path.exists(logo_path):
        _, center_col, _ = st.sidebar.columns([1, 2, 1])
        with center_col:
            st.image(logo_path, width=220)
        logger.info("Logo displayed.")
    else:
        st.sidebar.markdown("### Logo Placeholder")
        logger.warning("Logo not found, displaying placeholder.")

# Function to display sidebar content
def display_sidebar_content() -> None:
    """Displays headers and footer content in the sidebar."""
    st.sidebar.markdown(
        """<h4 style='text-align: center;'>
            Digital I&C Risk Assessment<br>
            Software Common Cause Failure Analysis
        </h4>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <h4 style='text-align: center;'>© 2025 BAHAMAS</h4>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        """
        <div style="
            font-size: 0.8rem;
            line-height: 1.5;
            color: #5b6573;
            border-top: 1px solid #d9dde3;
            margin-top: 1rem;
            padding-top: 0.75rem;
        ">
            For help or feedback, contact
            <a href="mailto:congjian.wang@inl.gov">congjian.wang@inl.gov</a>.<br>
            Additional resources:
            <a href="https://github.inl.gov/congjian-wang/BAHAMAS">GitHub repository</a>
            and
            <a href="https://lwrs.inl.gov/content/uploads/11/2024/11/2448420.pdf">Report</a>.
        </div>
        """,
        unsafe_allow_html=True,
    )
    logger.info("Displayed sidebar content.")


if __name__ == "__main__":

    # Initialize session state if not already done
    if 'shared_data' not in st.session_state:
        st.session_state['shared_data'] = ''

    # Create a sidebar menu for navigation
    with st.sidebar:
        selected_page = option_menu(
            "BAHAMAS",
            ["Welcome","Preliminary Assessment", "Comprehensive  Assessment", "Software Quality Survey", "Common Cause Identification",  "Common Cause Evaluation"],
            icons=["house-door", "clipboard-data", "bar-chart-line", "ui-checks-grid", "diagram-3", "shield-check"],
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
    elif selected_page == "Common Cause Identification":
        cccg_generation.app()
    elif selected_page == "Software Quality Survey":
        Software_Quality_Survey.app()
    elif selected_page == "Common Cause Evaluation":
        cccg_survey.app()


    display_logo(logo_path)
    display_sidebar_content()
