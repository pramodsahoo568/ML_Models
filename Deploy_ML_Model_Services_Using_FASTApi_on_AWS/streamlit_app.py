# python -m streamlit run streamlit_app.py
# python -m streamlit run streamlit_app.py --server.enableXsrfProtection false

import streamlit as st
import requests
from scripts import s3

# Define the API endpoint
#http://0.0.0.0:8502/api/v1/sentiment_analysis
API_URL = "http://0.0.0.0:8502/api/v1/"


st.title("ML Model Serving Over REST API")

text = st.text_area("Enter Your Movie Review")
user_id = st.text_input("Enter user id", "")

data = {"texts": [text], "user_id": user_id}
print(data)

import requests
import json

url = "http://0.0.0.0:8502/api/v1/sentiment_analysis"
'''
'''
headers = {
  'Content-Type': 'application/json'
}
if st.button("Predict"):
    with st.spinner("Predicting... Please wait!!!"):
        response = requests.post(url=url, headers=headers,
                                 json=data)

        output = response.json()

    st.write(output)