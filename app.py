import streamlit as st
import requests
import json
import time
import uuid
from function import create_form_from_name

st.title("AI Form Generator")

st.write("This app creates a form using a static schema and provides a preview link.")

# team_bot_id = st.text_input("Enter Team Bot ID:", placeholder="e.g., 6e3050c0-ba1c-12ea-8d89-1b3a8a22c978")
# auth_key = st.text_input("Enter Authorization Key (Bearer Token):", type="password", placeholder="Enter your bearer token")


form_name = st.text_input("Enter Form Name:", placeholder="e.g., Customer Feedback Survey")

if st.button("Create Form"):
    # if not team_bot_id:
    #     st.warning("Please enter the Team Bot ID.")
    # elif not auth_key:
    #     st.warning("Please enter the Authorization Key.")
    if not form_name:
        st.warning("Please enter a form name.")
    else:
        st.info("Creating form...")
        result = create_form_from_name(form_name)


        if isinstance(result, str):
            st.success("Form created successfully!")
            st.write("Form Preview Link:")
            st.markdown(f"[{result}]({result})")
        elif isinstance(result, dict) and 'error' in result:
            st.error(f"Form creation failed: {result['error']}")
        else:
            st.error("An unexpected error occurred during form creation.")



