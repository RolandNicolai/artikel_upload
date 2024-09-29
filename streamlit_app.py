import streamlit as st

st.title("Auth demo!")


with st.echo():
    st.write("Is user logged in?", st.experimental_user.is_logged_in())

left, middle, right, logout_button_column = st.columns(4)


with left:
    google_button = st.button("Login with Google")

    if google_button:
        st.experimental_user.login(provider="google")


st.write(":sparkles: :rainbow[User data]")
st.write(st.experimental_user)


with logout_button_column:
    logout_button = st.button("Logout")
    if logout_button:
        st.experimental_user.logout()
