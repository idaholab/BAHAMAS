# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
import logging
import os

logger = logging.getLogger(__name__)


def display_logo(logo_path: str):
    """Displays the logo in the sidebar or a placeholder if the logo is not found.

    Args:
        logo_path (str): The file path for the logo image.
    """
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=220)
        logger.info("Logo displayed.")
    else:
        st.sidebar.markdown("### Logo Placeholder")
        logger.warning("Logo not found, displaying placeholder.")

# Function to display main content
def display_main_content():
    """Displays the main welcome content on the page."""
    st.title("Risk Assessment of Safety-Related Digital Instrumentation and Control Systems 📄")
    st.markdown(
        """
        Welcome to the Digital I&C Risk Assessment Platform 👋

        This app allows you to perform the following analyses.

        **Features:**
        - **Preliminary Assessment**: Software reliability assessment based on software development life cycle survey.
        - **Comprehensive  Assessment**: Software reliability assessment based on Bayesian belief network analysis of software development life cycle.
        - **Common Cause Analysis**: Software common cause analysis including common cause component group generation and evaluation.

        **Choose a page from the sidebar to begin!**
        """
    )
    logger.info("Displayed main welcome content.")

# Function to display sidebar content
def display_sidebar_content() -> None:
    """Displays headers and footer content in the sidebar."""
    st.sidebar.markdown(
        "<h2 style='text-align: center;'>Digital I&C Risk Assessment</h2>", unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<h4 style='text-align: center;'>Software Common Cause Failure Analysis</h4>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <div class="footer-text">
            © 2025 BAHAMAS
        </div>
        """,
        unsafe_allow_html=True,
    )
    logger.info("Displayed sidebar content.")


def app():
    display_logo("../docs/pics/bahamas_structure.png")
    display_sidebar_content()
    display_main_content()
