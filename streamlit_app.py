import streamlit as st
import hmac
import time
import pytz
from datetime import datetime
import streamlit_authenticator as stauth

# Load credentials from the Streamlit secrets
names = st.secrets["credentials"]["names"]
usernames = st.secrets["credentials"]["usernames"]
passwords = st.secrets["credentials"]["passwords"]

# Hash the passwords (if they are not already hashed)
hashed_passwords = stauth.Hasher(passwords).generate()

# Access the cookie name and signature key from secrets
cookie_name = st.secrets["auth"]["cookie_name"]
signature_key = st.secrets["auth"]["signature_key"]

# Check if all required values are present and correct
st.write(f"Names: {names}")
st.write(f"Usernames: {usernames}")
st.write(f"Hashed Passwords: {hashed_passwords}")
st.write(f"Cookie Name: {cookie_name}")
st.write(f"Signature Key: {signature_key}")

# Create the authenticator
authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

# Login method
name, authentication_status, username = authenticator.login("Login", "main")

# Handle login status
if authentication_status:
    authenticator.logout("Logout", "main")
    st.write(f"Welcome *{name}*")
    st.title("Some protected content")
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")



LOGO_URL_LARGE = "https://bonnierpublications.com/app/themes/bonnierpublications/assets/img/logo.svg"
st.logo(LOGO_URL_LARGE)
# Define the Copenhagen timezone
copenhagen_tz = pytz.timezone('Europe/Copenhagen')

# Get the current time in Copenhagen
current_time_copenhagen = datetime.now(pytz.utc).astimezone(copenhagen_tz)

# Extract the hour part as an integer
current_hour = current_time_copenhagen.hour

email = str(st.experimental_user.email)

if email and isinstance(email, str):
    first_name = email.split(".")[0]
else:
    first_name = ""
# Conditional statements based on the time of the day
if 6 <= current_hour < 10:
    st.title(":orange[Godmorgen] " + first_name.capitalize())
elif 10<= current_hour < 12:
    st.title(":orange[God formiddag] " + first_name.capitalize())
elif 12 <= current_hour < 18:
    st.title(":orange[God eftermiddag] " + first_name.capitalize())
else:
    st.title(":orange[Godaften] " + first_name.capitalize())

