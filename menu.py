import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/1_Home.py", label="Home")
    st.sidebar.page_link("pages/2_Season_Statistics.py", label="Statistics")
    st.sidebar.page_link("pages/3_Match_Center.py", label="Match Center")
    st.sidebar.page_link("pages/4_Player_Radar.py", label="Player Radar")
    st.sidebar.page_link("pages/5_Log_Out.py", label="Log Out")

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.switch_page("app.py")

def home_menu():
    # Show a navigation menu for unauthenticated users
    st.switch_page("pages/1_Home.py")

def menu():
    return authenticated_menu()

def out_menu():
    return unauthenticated_menu()
