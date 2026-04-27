

import os
from typing import List

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from state import State
from tools.folder_structure import folder_structure

class CulpritDiscovery(BaseModel):
    file_paths: List[str] = Field(description="The actual file paths")
    
def find_culprit_files(state:State):
    llm = ChatOllama(
        model="llama3",
        temperature=0,
        base_url=os.getenv("OLLAMA_BASE_URL") 
    )
    
    structured_llm = llm.with_structured_output(CulpritDiscovery)
    project_map = folder_structure(os.getenv("PROJECT_PATH"))
    prompt = f"""
    Identify the files responsible for this issue.
    Title: {state.issue_title}
    Description: {state.issue_description}
    FileStrucuture:{project_map}
    """
    
    try:
        result = structured_llm.invoke(prompt)
        print(result,)
        return {
            "related_files": list(result.file_paths),
            "status": "culprits_identified"
        }
    except Exception as e:
        print(f"Error in structured output: {e}")
        return {"status": "error_in_analysis"}
    