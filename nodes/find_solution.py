import os
from state import State
from typing import List

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from tools.fetch_code import fetch_code


class solution_struct(BaseModel):
    approach:str =Field(description="the step by step solution to fix the issue should be descriptive")
    branch_name:str = Field(description="Appropriate git branch name for the issue")
    commit_message:str =Field(description="Appropriate commit message for the issue")
    sed_commands:List[str] =Field(description="list of sed command to fix the issue")

def find_solution(state:State):
    llm = ChatOllama(
    model="llama3",
    temperature=0,
    base_url=os.getenv("OLLAMA_BASE_URL") 
)

    structured_llm = llm.with_structured_output(solution_struct)
    related_code = fetch_code(state.grep_commands,"../"+os.getenv("PROJECT_PATH"))
    prompt = f"""
    Generate sed commands that can be ran on a terminal to fix the issue, all the generated commands are ran one after another so be careful while generating.
    Title: {state.issue_title}
    Description: {state.issue_description}
    related Files:{state.related_files}
    folderStructure:{state.folder_structure}
    related_code:{related_code}
    
    """

    try:
        result = structured_llm.invoke(prompt)
        print("This is proposed approach:\n")
        print(result.approach)
            
        return {
            "sed_commands": list(result.sed_commands),
            "approach":result.approach,
            "related_code":related_code,
            "branch_name":result.branch_name,
            "commit_message":result.commit_message,
            "status": "solution_generated"
        }
    except Exception as e:
        print(f"Error in structured output: {e}")
        return {"status": "error_in_analysis"}
    
    