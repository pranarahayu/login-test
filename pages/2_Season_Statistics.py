import streamlit as st
from menu import menu
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

menu()
st.title("This page is available to all users")
st.markdown(f"You are currently logged in")

if 'coor' not in st.session_state:
    st.session_state['coor'] = []

value = streamlit_image_coordinates('./data/lapangkosong2.jpg', width=617.65, height=400, key="local",)

if value is not None:
  coor = value['x'], value['y']
  if coor not in st.session_state['coor']:
    st.session_state['coor'].append(coor)
    st.experimental_rerun()

#coor.append(value)
#st.write(value)
#st.write(coor)
