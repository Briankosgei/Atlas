import streamlit as st


def apply_styles():

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0E1117;
        }

        .metric-card {
            background: #161B22;
            border: 1px solid #30363D;
            border-radius: 16px;
            padding: 1rem;
            text-align: center;
        }

        .section-header {
            margin-top: 1rem;
            margin-bottom: 0.5rem;
            padding-bottom: 0.25rem;
            border-bottom: 1px solid #30363D;
        }

        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )