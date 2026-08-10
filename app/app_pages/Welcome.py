# Copyright 2025, Battelle Energy Alliance, LLC  ALL RIGHTS RESERVED

import streamlit as st
import logging
import os
# container always at the bottom
from streamlit_extras.bottom_container import bottom

logger = logging.getLogger(__name__)

logo_path = "../docs/pics/BAHAMAS_color.png"

# Function to display main content
def display_main_content():
    """Displays the main welcome content on the page."""
    # st.title("Risk Assessment of Safety-Related Digital Instrumentation and Control Systems")
    st.image(logo_path)
    st.markdown(
        """
        <div style="
            padding: 1.4rem 1.6rem;
            border-radius: 14px;
            background: linear-gradient(135deg, #f3f7fb 0%, #e7eef6 100%);
            border: 1px solid #d4dfeb;
            margin-bottom: 1rem;
        ">
            <div style="
                font-size: 1.45rem;
                font-weight: 700;
                color: #16324f;
                padding-bottom: 0.85rem;
                margin-bottom: 0.65rem;
                border-bottom: 1px solid #dbe4ea;
            ">
                Welcome to the Digital I&amp;C Risk Assessment Workspace
            </div>
            <div style="
                font-size: 1rem;
                line-height: 1.7;
                color: #334e68;
            ">
                This platform supports structured evaluation of safety-related digital
                instrumentation and control systems through analysis workflows that span
                early screening, detailed quantification, software quality assessment,
                and common cause failure evaluation.
            </div>
            <div style="
                font-size: 1.45rem;
                font-weight: 700;
                color: #16324f;
                margin-top: 1rem;
                padding-bottom: 0.85rem;
                margin-bottom: 0.85rem;
                border-bottom: 1px solid #dbe4ea;
            ">
                Analysis and Evaluation Modules
            </div>
            <div style="
                color: #38506a;
                line-height: 1.75;
                margin-bottom: 0.65rem;
            ">
                <strong>Preliminary Assessment:</strong> supports rapid, stage-level SDLC evaluation.<br>
                <strong>Comprehensive Assessment:</strong> delivers refined software failure probability estimates.<br>
                <strong>Common Cause Analysis:</strong> identifies software-related common cause failure drivers.<br>
                <strong>Software Quality Survey:</strong> provides structured reliability attribute review.<br>
                <strong>CCCG Evaluation:</strong> measures vulnerability using qualitative and quantitative criteria.
            </div>
        </div>
        """
        ,
        unsafe_allow_html=True,
    )

    logger.info("Displayed main welcome content.")

    st.markdown(
        """
        <h4 style="text-align: center;">
            BAHAMAS: Bayesian Belief Network Structure
        </h4>
        """,
        unsafe_allow_html=True,
    )
    st.image('../docs/pics/bahamas_structure.png')


def app():

    display_main_content()
