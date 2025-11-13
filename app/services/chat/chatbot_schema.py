from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum

class ConversationState(str, Enum):
    START = "start"
    COUNTRY_SELECTION = "country_selection"
    PURPOSE_SELECTION = "purpose_selection"
    INFO_GATHERING = "info_gathering"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"
    END = "end"

class ImmigrationState(BaseModel):
    current_message: str
    current_step: ConversationState = ConversationState.START
    user_info: Optional[List[Dict[str, Any]]] = None

class chat_request(BaseModel):
    user_message: str
    session_id: Optional[str] = None
    state: Optional[ImmigrationState] = None

class chat_response(BaseModel):
    response: str
    status: str = "success"
    message: str = ""
    state: Optional[ImmigrationState] = None

