from typing import Annotated, List, Optional
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


def merge_paths(existing: List[str], new: List[str]) -> List[str]:
    return list(set(existing + new))

class State(BaseModel):

    issue_title: str = Field(..., description="The title of the GitHub issue")
    issue_description: str = Field(..., description="The full body/text of the issue")
    # issue_comments: List[str] = Field(default_factory=list)
    
    messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)
    
    related_files: Annotated[List[str], merge_paths] = Field(default_factory=list,description="List of files that might be causing the issue")
    
    approach: Optional[str] = Field(None, description="The planned strategy to fix the bug")
    modified_files: List[str] = Field(default_factory=list, description="List of files actually edited")

    status: str = Field(default="analyzing", description="Current stage: analyzing, planning, coding, or testing")



