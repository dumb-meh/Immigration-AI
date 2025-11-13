from pydantic import BaseModel
from typing import Optional,List

class affirmation_request(BaseModel):
    user_message:str
    information: Optional[List] = None

class affirmation_response(BaseModel):
    response:str
    status:str
    message:str

