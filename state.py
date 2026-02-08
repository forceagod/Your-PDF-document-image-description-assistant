"""Graph state definitions and data structures for the Deep Research agent."""

import operator
from typing import Annotated, Optional

from langchain_core.messages import MessageLikeRepresentation
from langgraph.graph import MessagesState
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


###################
# Structured Outputs
###################
class judge_out(BaseModel):
    reason_for_Judgment:str = Field(
        description="Reasons for judging whether the image is meaningful",
    )
    is_meaningful: bool = Field(
        description="Whether the image is meaningful.",
    )

class disc_image_out(BaseModel):
    """this model for disc a image"""
    need_info: bool = Field(
        description="Whether the information is insufficient to describe the image",
    )
    image_disc: str = Field(
        description="the discription of image",
    )

class summmary_image_info_from_context_out(BaseModel):
    """this model for summary info from context for given image"""
    need_extract: bool = Field(
        description="Whether the information is insufficient to describe the image",
    )
    image_info:str = Field(
        description="the info extracted from context base on the given image",
    )


###################
# State Definitions
###################

def override_reducer(current_value, new_value):
    """Reducer function that allows overriding values in state."""
    if isinstance(new_value, dict) and new_value.get("type") == "override":
        return new_value.get("value", new_value)
    else:
        return operator.add(current_value, new_value)
    
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


