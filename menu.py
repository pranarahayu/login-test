import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("1_Home.py", label="Statistics")
    st.sidebar.page_link("2_Season_Statistics.py", label="Statistics")

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("app.py", label="Log in")
