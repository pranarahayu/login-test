import streamlit as st
from menu import menu

menu()
st.title("This page is available to all users")
st.markdown(f"You are currently logged in")
