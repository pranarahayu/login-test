import sys
import io
import streamlit as st
import pandas as pd
import numpy as np
from tempfile import NamedTemporaryFile
import urllib

import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.patches as patches
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch
import seaborn as sns

from fungsi import proses_tl
from fungsi import get_sum90
from fungsi import get_pct
from fungsi import beli_pizza
from fungsi import player_dist

st.set_page_config(page_title='Player Radar', layout='wide')
st.markdown('# Player Radar')

from menu import menu
menu()

@st.cache_data(ttl=600)
def load_data(sheets_url):
  xlsx_url = sheets_url.replace("/edit#gid=", "/export?format=xlsx&gid=")
  return pd.read_excel(xlsx_url)

df = load_data(st.secrets["report"])
dx = load_data(st.secrets["timeline"])
xg = load_data(st.secrets["xg"])
db = load_data(st.secrets["player"])

col1, col2 = st.columns(2)
with col1:
  mins = st.number_input('Input minimum mins. played', min_value=90, max_value=3060, step=90, key=96)
  rank_p90 = get_sum90(df, dx, xg, db, mins)[0]
  rank_tot = get_sum90(df, dx, xg, db, mins)[1]
  abc = get_pct(rank_p90)

with col2:
  player = st.selectbox('Select Player', pd.unique(rank_p90['Name']), key='104')
  pos = rank_p90[rank_p90['Name']==player]['Position'].values[0]
  klub = rank_p90[rank_p90['Name']==player]['Team'].values[0]

col1, col2 = st.columns(2)
with col1:
  piz = beli_pizza('Liga 1', pos, klub, player, abc, mins)
  st.pyplot(piz)
  with open('pizza.jpg', 'rb') as img:
    fn = 'Perf.Radar_'+player+'.jpg'
    btn = st.download_button(label="Download Radar", data=img,
                             file_name=fn, mime="image/jpg")

with col2:
  dis = player_dist('Liga 1', pos, klub, player, rank_p90, mins)
  st.pyplot(dis)
  with open('dist.jpg', 'rb') as img:
    fn = 'Distribution_'+player+'.jpg'
    btn = st.download_button(label="Download Plot", data=img,
                             file_name=fn, mime="image/jpg")
