
from typing import Union

from fastapi import FastAPI
from fastapi import Request
import uvicorn
import os
import time
from transformers import  AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import requests
from data_module.data_schema import NLPDataInput, NLPDataOutput

MODEL_NAME = "ProsusAI/finbert"

# --------- Load tokenizer & model ----------
print("Load the model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

##print("Model config:", model.config)

# pipeline will handle tokenization and device placement
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print("Device:",device)
sentiment_pipe = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer,
    device=device
)


app = FastAPI()

@app.get("/")
def read_root():
    return "FastAPI Stock Sentiment Server is UP..."

@app.post("/api/v1/finance_sentiment_analysis")
def sentiment_analysis(data: NLPDataInput):
    print("sentiment_analysis /api/v1/finance_sentiment_analysis...")
    start = time.time()
    print(data.texts)
    result = sentiment_pipe(data.texts)
    print("Output:", result);
    end = time.time()
    prediction_time = int((end - start) * 1000)

    label = result[0]['label']
    score = result[0]['score']

    print("label:",label)
    print(type(label))
    print("score:", score)
    print(type(score))
    output = NLPDataOutput(model_name=MODEL_NAME,
                           label=label,
                           score=score,
                           prediction_time=prediction_time)
    return output


if __name__=="__main__":
    uvicorn.run(app="app:app", port=8503, reload=False, host="0.0.0.0")