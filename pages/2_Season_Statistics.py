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
df = pd.DataFrame(st.session_state['coor'])
#df = df.rename(columns={df.columns[0]:'X',df.columns[1]:'Y'})
#df['X'] = (df['X']*100)/xval
#df['Y'] = df['Y']/4

#st.write(df)

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(st.session_state['coor'])

def callback():
    edited_rows = st.session_state["data_editor"]["edited_rows"]
    rows_to_delete = []

    for idx, value in edited_rows.items():
        if value["x"] is True:
            rows_to_delete.append(idx)

    st.session_state["data"] = (
        st.session_state["data"].drop(rows_to_delete, axis=0).reset_index(drop=True)
    )


columns = st.session_state["data"].columns
column_config = {column: st.column_config.Column(disabled=True) for column in columns}

modified_df = st.session_state["data"].copy()
modified_df["x"] = False
# Make Delete be the first column
modified_df = modified_df[["x"] + modified_df.columns[:-1].tolist()]

st.data_editor(
    modified_df,
    key="data_editor",
    on_change=callback,
    hide_index=True,
    column_config=column_config,
)
