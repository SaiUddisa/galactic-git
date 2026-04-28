from typing import Annotated, List, Dict, Optional
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

def merge_paths(existing: List[str], new: List[str]) -> List[str]:
    return list(set(existing + new))

def merge_grep_map(existing: Dict[str, List[str]], new: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Merges two dictionaries. If a key (filepath) exists in both, 
    it combines the grep command arrays without duplicates.
    """
    updated = existing.copy()
    for file_path, commands in new.items():
        if file_path in updated:
            # Combine lists and remove duplicates
            updated[file_path] = list(set(updated[file_path] + commands))
        else:
            updated[file_path] = commands
    return updated

class State(BaseModel):
    issue_title: str = Field(..., description="The title of the GitHub issue")
    issue_description: str = Field(..., description="The full body/text of the issue")
    related_files: Annotated[List[str], merge_paths] = Field(default_factory=list,description="List of files that might be causing the issue")
    grep_commands: Annotated[List[str], merge_paths] = Field(default_factory=list,description="List of grep commands that will fetch the related lines of code")
    # Merged field: Key is filepath, Value is list of grep commands
    # file_grep_map: Annotated[Dict[str, List[str]], merge_grep_map] = Field(
    #     default_factory=dict,
    #     description="Mapping of file paths to the grep commands used to find relevant lines"
    # )
    
    approach: Optional[str] = Field(None, description="The planned strategy to fix the bug")
    modified_files: List[str] = Field(default_factory=list, description="List of files actually edited")
    status: str = Field(default="analyzing", description="Current stage: analyzing, planning, coding, or testing")