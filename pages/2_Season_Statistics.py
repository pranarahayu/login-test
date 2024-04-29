import streamlit as st
from menu import menu
from streamlit_image_coordinates import streamlit_image_coordinates

menu()
st.title("This page is available to all users")
st.markdown(f"You are currently logged in")

value = streamlit_image_coordinates('./data/lapangkosong2.jpg', width=772, height=500, key="local",)
#st.write(value)
