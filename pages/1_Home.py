import streamlit as st
from menu import menu
from st_supabase_connection import SupabaseConnection
import pandas as pd
from datetime import date, timedelta

menu()
st.title("This page is available to all users")
st.markdown(f"You are currently logged in")

conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM clubs;', ttl="10m")

st.write(df.head(10))
