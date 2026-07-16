import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .stApp{
        background-color:#0E1117;
    }

    div[data-testid="metric-container"]{
        background:#1C1F26;
        border:1px solid #2E3440;
        border-radius:15px;
        padding:18px;
        box-shadow:0px 4px 12px rgba(0,0,0,0.35);
    }

    h1,h2{
        color:#4CAF50;
    }

    h3{
        color:white;
    }

    .stProgress > div > div{
        background:#4CAF50;
    }

    section[data-testid="stSidebar"]{
        background:#161A23;
    }
    </style>
    """, unsafe_allow_html=True)