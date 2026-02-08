"""Graph state definitions and data structures for the Deep Research agent."""

import operator
from typing import Annotated, Optional

from langchain_core.messages import MessageLikeRepresentation
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


    
class AgentInputState(TypedDict):
    """InputState is only 'messages'."""
    image_path:str
    image_name:str
    mark_down_path:str
    image_context:str
    Number_of_check: int
    final_image_disc:str
    p_error:str

class AgentState(TypedDict):
    """Main agent state containing messages and research data."""
    image_path:str
    image_name:str
    mark_down_path:str
    image_context:str = ""
    Number_of_check: int = 0
    final_image_disc:str
    p_error:str



