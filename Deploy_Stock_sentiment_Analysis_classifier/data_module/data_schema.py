# accept the input params/data(text) payload
# output the score, class, latency

from pydantic import BaseModel

class NLPDataInput(BaseModel):
    texts : str
    user_id : str


class NLPDataOutput(BaseModel):
    model_name: str
    ##texts: str
    label: str
    score: float
    prediction_time: int



