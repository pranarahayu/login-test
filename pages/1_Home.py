import streamlit as st

st.title("This page is available to all users")
st.markdown(f"You are currently logged with the role of {st.session_state.role}.")
