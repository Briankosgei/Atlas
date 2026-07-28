import streamlit as st


def metric_card(title, value, color="white"):

    st.markdown(
        f"""
        <div class="metric-card">
            <div style="font-size:0.9rem;color:#8B949E;">{title}</div>
            <div style="font-size:2rem;font-weight:700;color:{color};">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title):

    st.markdown(
        f"<h3 class='section-header'>{title}</h3>",
        unsafe_allow_html=True,
    )