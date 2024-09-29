
import streamlit as st
import hmac
import time
import pytz
from datetime import datetime
from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

token_result = run_query("select * from `bonnier-deliverables.vertexAI_search.token_table`")



def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 Ukendt bruger eller adgangskode")
    return False

if not check_password():
    st.stop()



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
    st.title(":orange[Godmorgen] ")
elif 10<= current_hour < 12:
    st.title(":orange[God formiddag] ")
elif 12 <= current_hour < 18:
    st.title(":orange[God eftermiddag] ")
else:
    st.title(":orange[Godaften] ")



# Setup Google Cloud credentials
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["service_account"]
)

def upload_blob(bucket_name, file_obj, destination_blob_name):
    """Uploads a file to the bucket from a file-like object."""
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    # Upload the file directly from the file-like object
    blob.upload_from_file(file_obj, content_type="application/pdf")
    
    st.write(f"Fil blev uploadet: {bucket_name}/{destination_blob_name}.")

# Streamlit file uploader
uploaded_file = st.file_uploader("Vælg en PDF fil", type="pdf")

token_input = st.text_input(
        "Indsæt Token",
        "Indsæt unik token her",
        key="placeholder",
        )

#token = token_result["token"]  # Replace "token_column_name" with the actual column name you need
token_validation = token_result[0].get("token")  # Safely get the token if present
#st.write(token_1)# File name in cloud storage

if uploaded_file:
    destination_blob_name = uploaded_file.name
   #st.write("Navn på fil: ", uploaded_file.name);
# Handle file upload when button is clicked
if st.button("Upload fil"):
    if token_input == token_validation:
        # Call the upload_blob function with the file object
        upload_blob("vertex_search_assets", uploaded_file, destination_blob_name)
    else:
        st.error("Ingen fil valgt, vælg venligst en fil.")
