import streamlit as st
from menu import authenticated_menu, home_menu
import openpyxl
from openpyxl import load_workbook
import time
from io import BytesIO
import urllib

def load_workbook_from_url(url):
    file = urllib.request.urlopen(url).read()
    return load_workbook(filename = BytesIO(file))

wb = load_workbook_from_url(st.secrets["akses"]).worksheets[0]

# Create an empty container
placeholder = st.empty()

actual_email = "email"
actual_password = "password"

# Insert a form in the container
with placeholder.form("login"):
    st.markdown("#### Enter your credentials")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    timestamp = time.time()
    submit = st.form_submit_button("Login")

if submit and email == actual_email and password == actual_password:
    # If the form is submitted and the email and password are correct,
    # clear the form/container and display a success message
    placeholder.empty()
    row = [email,password,timestamp]
    wb.append_row(row)
    home_menu()
    st.success("Login successful")
    #authenticated_menu()
elif submit and email != actual_email and password != actual_password:
    st.error("Login failed")
else:
    pass
