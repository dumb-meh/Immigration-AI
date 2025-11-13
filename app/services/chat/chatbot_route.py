from fastapi import APIRouter, HTTPException
from .chatbot import Chatbot
from .chatbot_schema import affirmation_response, affirmation_request

router = APIRouter()
chatbot= Chatbot()  

@router.post("/chatbot", response_model=affirmation_response)
async def  get_affirmation(request: affirmation_request):
    try:
        response = chatbot.chat_with_AI(request.dict())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
