# accept the input params/data(text) payload
# output the score, class, latency

from pydantic import BaseModel

class NLPDataInput(BaseModel):
    texts : list[str]
    user_id : str


class NLPDataOutput(BaseModel):
    model_name: str
    texts: list[str]
    labels: list[str]
    scores: list[float]
    prediction_time: int



