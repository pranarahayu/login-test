import streamlit as st
import pandas as pd
import glob
from datetime import date
import numpy as np
from sklearn import preprocessing

from mplsoccer import Pitch, VerticalPitch, PyPizza, Radar, grid
import matplotlib.pyplot as plt

from PIL import Image
from tempfile import NamedTemporaryFile
import urllib
import os

from menu import menu

menu()
st.title("Untuk Konten LIB")

col1, col2, col3 = st.columns(3)
with col1:
    data = st.file_uploader("Upload file timeline excel!")
    try:
        tl = pd.read_excel(data, skiprows=[0])
    except ValueError:
        st.error("Please upload the timeline file")

with col2:
    teams = tl['Team'].unique().tolist()
    team = st.selectbox('Select Team', teams)

with col3:
    color = st.color_picker("Pick A Color", "#000000")

def draw_court(x_min=0, x_max=7.32,
               y_min=0, y_max=2.44,
               line_color='grey',
               line_thickness=15,
               grass_color='#0E7A0E',
               net_thick=2,
               max_v=16, max_h=8,
               ax=None
               ):

  lx1 = [x_min, x_max, x_max, x_min, x_min]
  ly1 = [y_min, y_min, y_max, y_max, y_min]
  lx2 = [x_min, x_max, x_max, x_min, x_min, x_max]
  ly2 = [y_min, y_min, y_max, y_max, y_min, y_min]

  garis = [[lx1, ly1], [lx2, ly2]]
  ax.axis('off')

  for line in garis:
    ax.plot(line[0], line[1],
            color=line_color,
            lw=line_thickness)

  ax.plot([x_min-0.75,x_max+0.75],[y_min,y_min],
          color=grass_color,
          lw=line_thickness)

  return ax

df = tl.copy()
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 12), dpi=500)
fig.subplots_adjust(hspace=-0.3, wspace=-0.3)
fig.patch.set_facecolor(color)
axs = axs.flatten()

for i in range(0,2):
  axs[i].set_facecolor(color)
  if i == 1:
    pitch = VerticalPitch(pitch_type='wyscout', pitch_color=color, line_color='#FFFFFF',
                          corner_arcs=True, goal_type='circle', linewidth=2, half=True, pad_bottom=0.2)
    pitch.draw(ax=axs[i])
    df_team = df[df['Team'] == team].reset_index(drop=True)
    for j in range(len(df_team)):
      if (df_team['Action'][j] == 'penalty goal') or (df_team['Action'][j] == 'goal'):
        axs[i].scatter(df_team['Y1'][j], df_team['X1'][j], s=100,
                       c='#FFFFFF', marker='o', lw=1, ec='#0F528C')
      elif (df_team['Action'][j] == 'shoot on target'):
        axs[i].scatter(df_team['Y1'][j], df_team['X1'][j], s=100,
                       c='#FFFFFF', marker='H', lw=1, ec='#0F528C')
      elif (df_team['Action'][j] == 'shoot off target'):
        axs[i].scatter(df_team['Y1'][j], df_team['X1'][j], s=100,
                       c='#FFFFFF', marker='X', lw=1, ec='#0F528C')
      elif (df_team['Action'][j] == 'shoot blocked'):
        axs[i].scatter(df_team['Y1'][j], df_team['X1'][j], s=100,
                       c='#FFFFFF', marker='s', lw=1, ec='#0F528C')
  else:
    draw_court(x_min=0, x_max=7.32*0.5,
               y_min=0, y_max=2.44*0.5,
               line_color='#FFFFFF',
               grass_color='#F58220',
               line_thickness=7,
               net_thick=0.75,
               max_v=16, max_h=8,
               ax=axs[i])
    axs[i].axes.set_aspect('equal')
    df_team = df[df['Team'] == team].reset_index(drop=True)
    df_team['P'] = df_team['P']*((7.32*0.5)/100)
    df_team['Q'] = (100-df_team['Q'])*((2.44*0.5)/100)
    for x in range(len(df_team)):
      if df_team['Sub 1'][x] != 'Woodwork':
        if df_team['P'][x] == 0:
          df_team['P'][x] = df_team['P'][x]-0.25
        elif df_team['P'][x] == (7.32*0.5):
          df_team['P'][x] = df_team['P'][x]+0.25
        elif df_team['Q'][x] == (2.44*0.5):
          df_team['Q'][x] = df_team['Q'][x]+0.25
    for j in range(len(df_team)):
      if (df_team['Action'][j] == 'penalty goal') or (df_team['Action'][j] == 'goal'):
        axs[i].scatter(df_team['P'][j], df_team['Q'][j], s=100,
                       c='#FFFFFF', marker='o', lw=1, ec='#0F528C')
      elif (df_team['Action'][j] == 'shoot on target'):
        axs[i].scatter(df_team['P'][j], df_team['Q'][j], s=100,
                       c='#FFFFFF', marker='H', lw=1, ec='#0F528C')
      elif (df_team['Action'][j] == 'shoot off target'):
        axs[i].scatter(df_team['P'][j], df_team['Q'][j], s=100,
                       c='#FFFFFF', marker='X', lw=1, ec='#0F528C', zorder=2)
plt.savefig('pizza.jpg', dpi=500, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
st.pyplot(fig)
with open('pizza.jpg', 'rb') as img:
    fn = 'Attempts Map_'+team+'.jpg'
    btn = st.download_button(label="Download Image", data=img,
                             file_name=fn, mime="image/jpg")
