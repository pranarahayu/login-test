import streamlit as st
from menu import menu
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw
import pandas as pd

menu()
st.title("This page is available to all users")
st.markdown(f"You are currently logged in")

if 'coor' not in st.session_state:
    st.session_state['coor'] = []

xval = 617.6470588235249
yval = 400

value = streamlit_image_coordinates('./data/lapangkosong2.jpg', width=xval, height=yval, key="local",)

if value is not None:
  coor = value['x'], value['y']
  if coor not in st.session_state['coor']:
    st.session_state['coor'].append(coor)
    st.experimental_rerun()
#st.write(st.session_state['coor'])
df = pd.DataFrame(st.session_state['coor'])
df = df.rename(columns={df.columns[0]:'X',df.columns[1]:'Y'})
df['X'] = (df['X']*100)/xval
df['Y'] = df['Y']/4
if st.button('Delete last'):
    df = df.head(-1)
    st.write(df)
st.write(df)
#coor.append(value)
#st.write(value)
#st.write(coor)
