import streamlit as st
from menu import authenticated_menu, home_menu
import openpyxl
from openpyxl import load_workbook
from datetime import datetime
from st_supabase_connection import SupabaseConnection

conn = st.connection("supabase",type=SupabaseConnection)

# Create an empty container
placeholder = st.empty()

actual_email = "email"
actual_password = "password"

# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Enter your credentials")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    c = datetime.now()
    waktus = c.strftime('%H:%M:%S')
    tanggals = c.strftime('%Y-%m-%d')
    submit = st.form_submit_button("Login")

if submit and email == actual_email and password == actual_password:
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    placeholder.empty()
    #conn.table("mytable").insert([{"name":email, "pword":password, 'waktu':waktus, 'tanggal':tanggals}], count="None").execute()
    home_menu()
    st.success("Login successful")
    #authenticated_menu()
elif submit and email != actual_email and password != actual_password:
    st.error("Login failed")
else:
    pass
