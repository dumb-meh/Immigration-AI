import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from .chatbot_schema import chat_response, ImmigrationState, ConversationState

load_dotenv()

class ImmigrationChatbot:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=1000,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.graph = self._create_graph()
    
    def _create_graph(self):
        """Create the LangGraph workflow"""
        workflow = StateGraph(ImmigrationState)
        
        # Add nodes
        workflow.add_node("start", self._start_node)
        workflow.add_node("country_selection", self._country_selection_node)
        workflow.add_node("purpose_selection", self._purpose_selection_node)
        workflow.add_node("info_gathering", self._info_gathering_node)
        workflow.add_node("analysis", self._analysis_node)
        workflow.add_node("recommendation", self._recommendation_node)
        
        # Add edges
        workflow.set_entry_point("start")
        workflow.add_edge("start", "country_selection")
        workflow.add_edge("country_selection", "purpose_selection")
        workflow.add_edge("purpose_selection", "info_gathering")
        workflow.add_edge("info_gathering", "analysis")
        workflow.add_edge("analysis", "recommendation")
        workflow.add_edge("recommendation", END)
        
        return workflow.compile()
    
    def _get_user_info(self, state: ImmigrationState, key: str) -> Any:
        """Helper to get user info by key"""
        if not state.user_info:
            return None
        for info in state.user_info:
            if key in info:
                return info[key]
        return None
    
    def _add_user_info(self, state: ImmigrationState, key: str, value: Any) -> None:
        """Helper to add user info"""
        if not state.user_info:
            state.user_info = []
        state.user_info.append({key: value})
    
    def _start_node(self, state: ImmigrationState) -> ImmigrationState:
        """Initial greeting and introduction"""
        response = "🏆 Hi! I'm Immigration AI Assistant. Let's find the perfect visa for you."
        state.current_message = response
        state.current_step = ConversationState.COUNTRY_SELECTION
        return state
    
    def _country_selection_node(self, state: ImmigrationState) -> ImmigrationState:
        """Handle country selection"""
        destination_country = self._get_user_info(state, "destination_country")
        
        if not destination_country:
            response = "Nice. Which country are you applying to?"
            state.current_step = ConversationState.COUNTRY_SELECTION
        else:
            response = f"Great! You're applying to {destination_country}. What's the purpose of your visit?"
            state.current_step = ConversationState.PURPOSE_SELECTION
        
        state.current_message = response
        return state
    
    def _purpose_selection_node(self, state: ImmigrationState) -> ImmigrationState:
        """Handle purpose selection"""
        purpose = self._get_user_info(state, "purpose")
        
        if not purpose:
            response = "What is the purpose of your visit? Study Visa, Work Visa, Tourism, Business, or Family Visit?"
            state.current_step = ConversationState.PURPOSE_SELECTION
        else:
            response = f"Perfect! You're looking for a {purpose}. Which country are you currently living in?"
            state.current_step = ConversationState.INFO_GATHERING
        
        state.current_message = response
        return state
    
    def _info_gathering_node(self, state: ImmigrationState) -> ImmigrationState:
        """Gather additional user information"""
        current_country = self._get_user_info(state, "current_country")
        application_status = self._get_user_info(state, "application_status")
        applicant_type = self._get_user_info(state, "applicant_type")
        
        if not current_country:
            response = "Which country are you currently living in?"
        elif application_status is None:
            response = "Have you already started any visa application?"
        elif not applicant_type:
            response = "Are you applying for yourself or someone else?"
        else:
            response = "Have you ever applied for this visa before?"
            state.current_step = ConversationState.ANALYSIS
        
        state.current_message = response
        return state
    
    def _analysis_node(self, state: ImmigrationState) -> ImmigrationState:
        """Analyze user information"""
        destination = self._get_user_info(state, "destination_country")
        purpose = self._get_user_info(state, "purpose")
        current_country = self._get_user_info(state, "current_country")
        
        response = f"""Great! What is the purpose of your visit?
        
Based on your information:
- Applying to: {destination}
- Purpose: {purpose} 
- Current location: {current_country}

I'm analyzing your requirements..."""
        
        state.current_message = response
        state.current_step = ConversationState.RECOMMENDATION
        return state
    
    def _recommendation_node(self, state: ImmigrationState) -> ImmigrationState:
        """Provide visa recommendations"""
        response = """Perfect! I've gathered your basic info. Based on your answers, I can recommend the exact visa form you should fill and walk you through each step so you don't make any mistakes.

To continue, please unlock your personalized immigration AI assistant. It'll guide you through your official immigration form.

💼 Buy I Form    💰 Buy Family Package"""
        
        state.current_message = response
        state.current_step = ConversationState.END
        return state
    
    def chat_with_AI(self, user_message: str, current_state: ImmigrationState = None) -> chat_response:
        """Main chat interface"""
        if current_state is None:
            current_state = ImmigrationState()
        
        # Process user input first
        if current_state.current_step != ConversationState.START:
            current_state = self._process_user_input(user_message, current_state)
        
        # Run through graph nodes
        if current_state.current_step == ConversationState.START:
            current_state = self._start_node(current_state)
            current_state = self._country_selection_node(current_state)
        elif current_state.current_step == ConversationState.COUNTRY_SELECTION:
            current_state = self._country_selection_node(current_state)
        elif current_state.current_step == ConversationState.PURPOSE_SELECTION:
            current_state = self._purpose_selection_node(current_state)
        elif current_state.current_step == ConversationState.INFO_GATHERING:
            current_state = self._info_gathering_node(current_state)
        elif current_state.current_step == ConversationState.ANALYSIS:
            current_state = self._analysis_node(current_state)
        elif current_state.current_step == ConversationState.RECOMMENDATION:
            current_state = self._recommendation_node(current_state)
        
        return chat_response(
            response=current_state.current_message,
            status="success",
            message="Chat processed successfully",
            state=current_state
        )
    
    def _process_user_input(self, user_message: str, state: ImmigrationState) -> ImmigrationState:
        """Process user input based on current conversation step"""
        if state.current_step == ConversationState.COUNTRY_SELECTION:
            countries = {
                "united states": "United States", 
                "canada": "Canada", 
                "united kingdom": "United Kingdom", 
                "australia": "Australia"
            }
            for country_key, country_name in countries.items():
                if country_key in user_message.lower():
                    self._add_user_info(state, "destination_country", country_name)
                    break
        
        elif state.current_step == ConversationState.PURPOSE_SELECTION:
            purposes = {
                "study": "Study Visa",
                "work": "Work Visa", 
                "tourism": "Tourism",
                "business": "Business", 
                "family": "Family Visit"
            }
            for purpose_key, purpose_name in purposes.items():
                if purpose_key in user_message.lower():
                    self._add_user_info(state, "purpose", purpose_name)
                    break
        
        elif state.current_step == ConversationState.INFO_GATHERING:
            current_country = self._get_user_info(state, "current_country")
            application_status = self._get_user_info(state, "application_status")
            
            if not current_country:
                # Extract country from message (simplified)
                self._add_user_info(state, "current_country", user_message.strip())
            elif application_status is None:
                self._add_user_info(state, "application_status", "yes" in user_message.lower())
            else:
                self._add_user_info(state, "applicant_type", "myself" if "myself" in user_message.lower() else "someone else")
        
        return state
