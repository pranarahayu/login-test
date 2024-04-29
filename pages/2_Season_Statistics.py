import streamlit as st
from menu import menu
from streamlit_image_coordinates import streamlit_image_coordinates

menu()
st.title("This page is available to all users")
st.markdown(f"You are currently logged in")

coor = []
value = streamlit_image_coordinates('./data/lapangkosong2.jpg', width=617.65, height=400, key="local",)
coor.append(value)
st.write(value)
st.write(coor)
