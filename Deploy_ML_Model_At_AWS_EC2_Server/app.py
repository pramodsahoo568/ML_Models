import streamlit as st
import os
import torch
from transformers import pipeline


###Run Application
###>streamlit run app.py


import boto3
import  os
s3 = boto3.client('s3')

print("List Out S3 Bucket...")
response = s3.list_buckets()
print(response)
bucket_name = 'mlops-models'


local_path = 'tinybert-sentiment-analysis-model'
s3_prefix = 'ml-models/tinybert-sentiment-analysis-model/'

def download_dir(local_path, s3_prefix):
    os.makedirs(local_path, exist_ok=True)
    paginator = s3.get_paginator('list_objects_v2')
    for result in paginator.paginate(Bucket=bucket_name, Prefix=s3_prefix):
        if 'Contents' in result:
            for key in result['Contents']:
                s3_key = key['Key']

                local_file = os.path.join(local_path, os.path.relpath(s3_key, s3_prefix))
                # os.makedirs(os.path.dirname(local_file), exist_ok=True)

                s3.download_file(bucket_name, s3_key, local_file)

##print("Download directory to local folder")
st.title("Machine Learning Model Deployment at the Server!!!")

button = st.button("Download Model")
if button:
    with st.spinner("Downloading... Please wait!"):
        download_dir(local_path, s3_prefix)


text = st.text_area("Enter Your Review")
predict = st.button("Predict")

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
classifier = pipeline('text-classification', model='tinybert-sentiment-analysis-model', device=device)
if predict:
    with st.spinner("Predicting..."):
        output = classifier(text)
        st.write(output)
