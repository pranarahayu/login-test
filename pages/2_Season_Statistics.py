import streamlit as st
from menu import menu
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw
import pandas as pd

menu()
st.title("Untuk Konten LIB")

col1, col2 = st.columns(2)
with col1:
    data = st.file_uploader("Upload file timeline excel!")
    try:
        tl = pd.read_excel(data, skiprows=[0])
    except ValueError:
        st.error("Please upload the timeline file")

with col2:
    team = tl['Team'].unique().tolist()
    filter = st.selectbox('Select Team', team)

df = tl.copy()
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(10, 12), dpi=500)
fig.subplots_adjust(hspace=-0.3, wspace=-0.3)
fig.patch.set_facecolor('#0F528C')
axs = axs.flatten()

for i in range(0,2):
  axs[i].set_facecolor('#0F528C')
  if i == 1:
    pitch = VerticalPitch(pitch_type='wyscout', pitch_color='#0F528C', line_color='#FFFFFF',
                          corner_arcs=True, goal_type='circle', linewidth=2, half=True)
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

st.pyplot(fig)
