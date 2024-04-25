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
df = pd.DataFrame(rows)
st.write(df)
st.write(rows)
