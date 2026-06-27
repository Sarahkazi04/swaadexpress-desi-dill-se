import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import json
import requests

# Initialize Firebase
cred = credentials.Certificate('swaad-b5569-7de08b13c5df.json')
firebase_admin.initialize_app(cred)

def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    }
    if username:
        payload["displayName"] = username
    payload = json.dumps(payload)
    r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
    try:
        data = r.json()
        if 'email' in data:
            return data['email']
        else:
            st.warning(data.get('error', {}).get('message', 'An error occurred during sign-up.'))
    except Exception as e:
        st.warning(f'Sign-up failed: {e}')

def sign_in_with_email_and_password(email, password, return_secure_token=True):
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    payload = {
        "returnSecureToken": return_secure_token,
        "email": email,
        "password": password
    }
    payload = json.dumps(payload)
    r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
    try:
        data = r.json()
        if 'email' in data:
            user_info = {
                'email': data['email'],
                'username': data.get('displayName')
            }
            return user_info
        else:
            st.warning(data.get('error', {}).get('message', 'An error occurred during sign-in.'))
    except Exception as e:
        st.warning(f'Sign-in failed: {e}')

def customer_form():
    with st.form("customer_form"):
        st.write("Customer Details")

        # Input fields for customer information
        customer_name = st.text_input("Customer Name")
        customer_phone = st.text_input("Customer Phone Number")

        # Checklist for 2 tiffin service
        agree_to_tiffin_service = st.checkbox("Agree to 2 tiffin service")

        # Input fields for pickup and delivery addresses
        pickup_address = st.text_input("Pickup Address")
        delivery_address = st.text_input("Delivery Address")

        # Checklist for dabbawala service
        availing_dabbawala = st.checkbox("Currently availing the service of a dabbawala")
        if availing_dabbawala:
            dabbawala_name = st.text_input("Dabbawala's Name")
            dabbawala_contact = st.text_input("Dabbawala's Contact Number")

        # Submit button for the form
        submitted = st.form_submit_button("Submit")

        # Handle form submission
        if submitted:
            st.success("Customer Details Submitted")
            st.write(f"Name: {customer_name}")
            st.write(f"Phone Number: {customer_phone}")
            st.write(f"Agree to 2 tiffin service: {agree_to_tiffin_service}")
            st.write(f"Pickup Address: {pickup_address}")
            st.write(f"Delivery Address: {delivery_address}")
            if availing_dabbawala:
                st.write(f"Dabbawala's Name: {dabbawala_name}")
                st.write(f"Dabbawala's Contact Number: {dabbawala_contact}")

def dabbawalla_form():
    with st.form("dabbawalla_form"):
        st.write("Dabbawalla Details")

        # Input fields for dabbawalla information
        dabbawalla_name = st.text_input("Dabbawalla Name")
        dabbawalla_contact = st.text_input("Dabbawalla Contact")
        home_address = st.text_input("Home Address")

        # Submit button for the form
        submitted = st.form_submit_button("Submit")

        # Handle form submission
        if submitted:
            st.success("Dabbawalla Details Submitted")
            st.write(f"Dabbawalla Name: {dabbawalla_name}")
            st.write(f"Contact: {dabbawalla_contact}")
            st.write(f"Home Address: {home_address}")

def account_page():
    st.title("Account Page")
    st.write("Choose an option:")

    choice = st.radio("Select Account Type", ["Customer", "Dabbawala"])
    operation = st.radio(f"Would you like to sign up or log in as a {choice}?", ["Sign Up", "Log In"])

    if operation == "Sign Up":
        email = st.text_input("Email Address")
        password = st.text_input("Password", type='password')
        username = st.text_input("Username (optional)")

        if st.button(f"Sign Up as {choice}"):
            if st.session_state.get('usertype') == choice:
                st.warning("Account already exists in this type")
            else:
                user_email = sign_up_with_email_and_password(email, password, username)
                if user_email:
                    st.success(f"Successfully created an account as {choice}!")
                    st.balloons()
                    st.experimental_rerun()  # Refresh page to show login page

    elif operation == "Log In":
        email = st.text_input("Email Address")
        password = st.text_input("Password", type='password')

        if st.button(f"Log In as {choice}"):
            if st.session_state.get('usertype') and st.session_state['usertype'] != choice:
                st.warning("Login failed: Account already exists in another type")
            else:
                user_info = sign_in_with_email_and_password(email, password)
                if user_info:
                    st.session_state.username = user_info['username']
                    st.session_state.useremail = user_info['email']
                    st.session_state.usertype = choice
                    st.success(f"Successfully logged in as {choice}!")
                    st.experimental_rerun()  # Refresh page to show the form page

def app():
    st.title('Welcome to SwaadExpress :sunglasses:')

    # Initialize session state
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'usertype' not in st.session_state:
        st.session_state.usertype = ''

    if not st.session_state.username:
        account_page()
    else:
        st.write(f'Logged in as: {st.session_state.username}')
        if st.button('Logout'):
            st.session_state.username = ''
            st.session_state.useremail = ''
            st.session_state.usertype = ''
            st.experimental_rerun()
        
        # Display appropriate form based on user type
        if st.session_state.usertype == 'Customer':
            customer_form()
        elif st.session_state.usertype == 'Dabbawalla':
            dabbawalla_form()

if __name__ == '_main_':
    app()