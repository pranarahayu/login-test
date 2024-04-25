import streamlit as st
from menu import menu
from st_supabase_connection import SupabaseConnection
import pandas as pd

menu()
st.title("This page is available to all users")
st.markdown(f"You are currently logged in")

# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

# Perform query.
rows = conn.query("*", table="mytable", ttl="10m").execute()
df = pd.DataFrame(rows.data)
temp = df[['tanggal','name']]
temp = temp.groupby(['tanggal'], as_index=False).count()
st.line_chart(temp, x="tanggal", y="name")
st.write('last accessed by '+df['name'][len(df)-1]+' at '+df['tanggal'][len(df)-1]+' - '+df['waktu'][len(df)-1])
