import streamlit as st
import requests

# Backend API base URL
API_BASE_URL = "http://localhost:8000/api/v1/"

st.set_page_config(page_title="Auth App", page_icon="🔐")

st.title("🔐 Authentication App")

tab1, tab2 = st.tabs(["Login", "Register"])


# ---------------- LOGIN ----------------
with tab1:
    st.subheader("Login")

    email = st.text_input("Email", key="login_email")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        payload = {
            "email": email,
            "username": username,
            "password": password
        }

        try:
            response = requests.post(f"{API_BASE_URL}auth/login", data=payload)

            if response.status_code == 200:
                st.success("Login Successful")
                st.json(response.json())
            else:
                st.error("Login Failed")
                st.json(response.json())

        except Exception as e:
            st.error(f"Error connecting to backend: {e}")


# ---------------- REGISTER ----------------
with tab2:
    st.subheader("Register")

    username = st.text_input("Username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        payload = {
            "username": username,
            "email": email,
            "password": password
        }


        try:
            response = requests.post(f"{API_BASE_URL}auth/register", json=payload)

            # Backend returns 201 Created on successful registration
            if response.status_code in (200, 201):
                st.success("Registration Successful")
                st.json(response.json())
            else:
                st.error("Registration Failed")
                st.json(response.json())

        except Exception as e:
            st.error(f"Error connecting to backend: {e}")