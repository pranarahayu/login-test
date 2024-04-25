import streamlit as st
from menu import menu
from st_supabase_connection import SupabaseConnection
import pandas as pd
from datetime import date

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
st.write('Terakhir diakses oleh: '+df['name'][len(df)-1]+' pada '+(df['tanggal'][len(df)-1]).strftime("%d%b%Y")+' pukul '+df['waktu'][len(df)-1])
