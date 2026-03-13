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
                font-size: 0.85rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #355c7d;
                margin-bottom: 0.45rem;
            ">
                BAHAMAS Platform
            </div>
            <div style="
                font-size: 1.45rem;
                font-weight: 700;
                color: #16324f;
                margin-bottom: 0.65rem;
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
        </div>
        """
        ,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            **Core Analyses**
            - **Preliminary Assessment** for rapid, stage-level SDLC evaluation
            - **Comprehensive Assessment** for refined failure probability estimates
            - **Common Cause Analysis** for identifying software-related CCF drivers
            """
        )
    with col2:
        st.markdown(
            """
            **Supporting Evaluations**
            - **Software Quality Survey** for structured reliability attribute review
            - **CCCG Evaluation** for qualitative and quantitative vulnerability assessment
            """
        )

    logger.info("Displayed main welcome content.")


def app():

    display_main_content()

    with bottom():
        st.markdown('''For help or feedback, contact congjian.wang@inl.gov.
                For more options and information, check out the
                [GitHub repository](https://github.inl.gov/congjian-wang/BAHAMAS) or
                [Report](https://lwrs.inl.gov/content/uploads/11/2024/11/2448420.pdf)
                ''')
