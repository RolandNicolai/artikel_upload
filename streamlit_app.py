import streamlit as st
st.title("Google Auth demo!")

if not st.experimental_user.is_logged_in():
    st.warning("User not logged in")

google_button = st.button ("Login with Google", type="primary")

if google_button:
    st. experimental_user. login (provider="google")

if st.experimental_user.is_logged_in():
    st.write(": sparkles: :rainbow[User data]")

st.write(st. experimental_user)
logout_button = st.button ("Logout")

if logout_button:
    st.experimental_ user.logout()
