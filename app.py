import streamlit as st
from menu import authenticated_menu
from streamlit_gsheets import GSheetsConnection
import time

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="Sheet1")

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
    st.success("Login successful")
    df.write({"User":email, "Password":password, "Timestamp":timestamp})
    authenticated_menu()
elif submit and email != actual_email and password != actual_password:
    st.error("Login failed")
else:
    pass
