import streamlit as st
from menu import menu
from st_supabase_connection import SupabaseConnection
import pandas as pd
from datetime import date, timedelta

menu()
st.title("This page is available to all users")
st.markdown(f"You are currently logged in")

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="mytable", ttl="10m").execute()
df = pd.DataFrame(rows.data)
df['tanggal'] = pd.to_datetime(df['tanggal'])
df['waktu'] = pd.to_datetime(df['waktu'])
temp = df[['tanggal','name']]
temp = temp.groupby(['tanggal'], as_index=False).count()
st.line_chart(temp, x="tanggal", y="name")
us = df['name'][len(df)-1]
tg = str((df['tanggal'][len(df)-1]).strftime("%d/%m/%Y"))
wts = (df['waktu'][len(df)-1])
jkt = wts + timedelta(hours=7)
wt = str(jkt.strftime("%X"))
st.write('Terakhir diakses oleh '+us+' pada '+tg+' pukul '+wt+' WIB')
