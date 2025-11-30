
from transformers import  AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import requests
import torch.nn.functional as F

MODEL_NAME = "ProsusAI/finbert"


# --------- Load tokenizer & model ----------
print("Load the model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Print config mapping (helps to know id2label)
##print("Model config:", model.config)

# pipeline will handle tokenization and device placement
pipe_device = 0 if torch.cuda.is_available() else -1
sentiment_pipe = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer,
    device=pipe_device
)

'''
Get The News from Web to prepare input text
'''

stock_keyword = "META"
data = "2025-11-29"



'''
---------------------------------------------------
Predict Text Code 
'''
text = (
    "Shares of Reliance Industries Ltd. (RIL) down 1.1% on Friday to hit a new 52-week low "
    "of Rs 1,580.90 on the BSE after global brokerage firm Jefferies reiterated its ‘sell’ rating "
    "on the stock with a price target of Rs 1,485, implying a potential down of 14%."
)
print("Text: ",text)
print("\n--- Pipeline Result ---")
pipeline_result = sentiment_pipe(text, truncation=True)
print(pipeline_result)
score = int(pipeline_result[0]['score']*100);
print("Sentiment: ",pipeline_result[0]['label'])
print(f"Score:{score} %",)