

import os
from typing import List

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from state import State
from tools.folder_structure import folder_structure

class CulpritDiscovery(BaseModel):
     file_paths: List[str] = Field(description="The actual file paths")
     grep_commands: List[str] = Field(description="Grep commands that will fetch the related lines of code")
    
def find_culprit_files(state:State):
    llm = ChatOllama(
        model="llama3",
        temperature=0,
        base_url=os.getenv("OLLAMA_BASE_URL") 
    )
    
    structured_llm = llm.with_structured_output(CulpritDiscovery)
    project_map = folder_structure(os.getenv("PROJECT_PATH"))
    prompt = f"""
    Identify the files(with relevent paths) responsible for this issue and Grep commands to find the line of code  in those files that  causing the issue.
    Title: {state.issue_title}
    Description: {state.issue_description}
    FileStrucuture:{project_map}
    """
    
    try:
        result = structured_llm.invoke(prompt)
        print("These files might be causing the issue:\n")
        for path in result.file_paths:
            print(path)
            
        return {
            "related_files": list(result.file_paths),
            "folder_structure":project_map,
            "grep_commands":result.grep_commands,
            "status": "culprits_identified"
        }
    except Exception as e:
        print(f"Error in structured output: {e}")
        return {"status": "error_in_analysis"}
    