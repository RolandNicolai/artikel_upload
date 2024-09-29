import streamlit as st
import hmac
import time
import pytz
from datetime import datetime
import streamlit_authenticator as stauth

# Access the credentials directly from the secrets
names = st.secrets["credentials"]["names"]
usernames = st.secrets["credentials"]["usernames"]
passwords = st.secrets["credentials"]["passwords"]

cookie_name = st.secrets["credentials"]["cookie_name"]
signature_key = st.secrets["credentials"]["signature_key"]

# Hash the passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# Authenticate using the credentials
authenticator = stauth.Authenticate(
    names, 
    usernames, 
    hashed_passwords, 
    'cookie_name', 
    'signature_key', 
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

# Handle authentication status
if st.session_state['authentication_status']:
    authenticator.logout('Logout', 'main')
    st.write(f"Welcome *{st.session_state['name']}*")
    st.title('Some content')
elif st.session_state['authentication_status'] == False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] == None:
    st.warning('Please enter your username and password')


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

