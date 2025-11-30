# python -m streamlit run ui_app.py
# python -m streamlit run ui_app.py --server.enableXsrfProtection false

import streamlit as st
import requests

# Define the API endpoint
url = "http://0.0.0.0:8503/api/v1/finance_sentiment_analysis"



page_bg_color = """
<style>
.stApp {
    background-color: #99adcc;   /* change color here */
}
</style>
"""

st.markdown(page_bg_color, unsafe_allow_html=True)
st.title("Finance Model Stock Sentiment Analysis")


text = st.text_area("Enter Your Stock News")
user_id = ""##st.text_input("Enter user id", "")

data = {"texts": text, "user_id": user_id}
print(data)

import requests
import json


'''
'''
headers = {
  'Content-Type': 'application/json'
}

st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #002699;      /* Green */
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 10em;
    font-size: 16px;
}
div.stButton > button:hover {
    background-color: #45a049;
    color: white;
}
</style>
""", unsafe_allow_html=True)

if st.button("Predict"):
    with st.spinner("Predicting... Please wait!!!"):
        response = requests.post(url=url, headers=headers,
                                 json=data)
        output = response.json()
        sentiment_label = output['label'];
        score = output['score']
        print(sentiment_label)
    if sentiment_label == "positive" :
        recommendation = "Buy"
    else:
        recommendation = "Sell"

    result = f"<b>Sentiment: {sentiment_label}<br><b>Stock recommendation: {recommendation}"
    st.markdown(result, unsafe_allow_html=True)