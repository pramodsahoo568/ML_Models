from typing import Union

from fastapi import FastAPI
from fastapi import Request
import uvicorn
import os
import time

from transformers import  pipeline
import torch

from scripts.data_model import NLPDataInput, NLPDataOutput
from scripts import s3



####   DownLoad ML Model  Start #####


force_download =  False; ## True
##local_path = 'tinybert-sentiment-analysis-model'
##s3_prefix = 'ml-models/tinybert-sentiment-analysis-model/'
model_name = 'tinybert-sentiment-analysis-model'
local_path = 'ml_models/'+model_name
if not os.path.isdir(local_path) or force_download:
    s3.download_dir(local_path, model_name)
else:
    print("Model Already Exist...")



####   DownLoad ML Model  End #####

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

## load an initialize models for inference
print("Initialize sentiment model...")
sentiment_model = pipeline('text-classification', model=local_path, device=device)


app = FastAPI()

@app.get("/")
def read_root():
    return "FastAPI Server is UP..."

@app.post("/api/v1/sentiment_analysis")
def sentiment_analysis(data: NLPDataInput):
    start = time.time()
    output = sentiment_model(data.texts)
    end = time.time()
    prediction_time = int((end - start) * 1000)

    labels = [x['label'] for x in output]
    scores = [x['score'] for x in output]

    output = NLPDataOutput(model_name=model_name,
                           texts=data.texts,
                           labels=labels,
                           scores=scores,
                           prediction_time=prediction_time)
    return output

@app.post("/api/v1/disaster_classifier")
def disaster_classifier(data: NLPDataInput):
    return data

if __name__=="__main__":
    uvicorn.run(app="app:app", port=8502, reload=False, host="0.0.0.0")

