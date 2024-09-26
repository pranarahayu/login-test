import streamlit as st
from menu import menu
from PIL import Image, ImageDraw
import pandas as pd

st.set_page_config(page_title='Match Center', layout='wide')
st.markdown('# Match Center')

from menu import menu
menu()

col1, col2, col3, col4 = st.columns(4)
with col1:
  ssn = st.selectbox('Select Season', ['2021/22', '2022/23', '2023/24', '2024/25'], key='1')
with col2:
  komp = st.selectbox('Select Competition', ['Liga 1', 'Liga 2'], key='2')
with col3:
  gw = st.selectbox('Select Gameweek', [1, 2, 3, 4], key='3')
with col4:
  match = st.selectbox('Select Match', ['PERSIB Bandung vs PSBS Biak'], key='4')

col1, col2, col3 = st.columns(3)
with col1:
  st.image('./data/pnet-persib.jpg')
with col2:
  st.image('./data/stats.jpg')
  st.image('./data/momentum.jpg')
with col3:
  st.image('./data/pnet-psbs.jpg')
