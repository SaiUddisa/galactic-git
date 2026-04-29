

import os
import sys
from typing import List

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from state import State
from tools.fetch_code import fetch_code
from tools.folder_structure import folder_structure

class CulpritDiscovery(BaseModel):
     file_paths: List[str] = Field(description="The actual file paths")
     grep_commands: List[str] = Field(description="Grep commands that will fetch the related lines of code")
    
def find_culprit_files(state:State):
    
    if(state.code_fetch_attempts >=20):
        print("\nMax hops reached !!!!")
        print(state.grep_commands)
        sys.exit()
    llm = ChatOllama(
        model="llama3",
        temperature=0,
        base_url=os.getenv("OLLAMA_BASE_URL") 
    )
    
    structured_llm = llm.with_structured_output(CulpritDiscovery)
    
    project_map = folder_structure(os.getenv("PROJECT_PATH"),state.code_fetch_attempts)
    prompt = f"""
   Identify the files (with relevant paths) responsible for this specific issue and provide precise grep commands to locate the exact lines of code causing it.

**Issue Details:**
- Title: {state.issue_title}
- Description: {state.issue_description}

**Codebase Structure:**
{project_map}

**Previous Attempts:**
- Previously tried grep commands: {state.grep_commands}
- Previously identified related files: {state.related_files}

**Instructions:**
1. Analyze the issue title and description to extract key error messages, function names, variables, stack traces, or patterns that likely cause the problem.
2. Based on the project structure, suggest 3-5 most probable files/directories where the issue originates (e.g., controllers, services, config files matching the issue context).
3. Provide 4-6 targeted grep commands as alternatives to previous attempts, using variations like:
   - Case-insensitive search: `grep -i "pattern" file_or_dir/`
   - Recursive with line numbers: `grep -rn "pattern" dir/`
   - Multiple patterns: `grep -E "pattern1|pattern2" dir/`
   - Context lines: `grep -C 3 "pattern" file`
   - Regex for stack traces/variables: `grep -r "function_name.*error" src/`
4. Prioritize searches in likely locations from the project structure (e.g., src/, app/, config/, tests/).
5. If previous greps failed, suggest broader searches (`-r`), regex patterns, or file-type filters (`--include="*.js"`).

Focus on efficiency: target probable files first and use grep flags to avoid false positives.
    """
    
    try:
        result = structured_llm.invoke(prompt)
        print("\nThese files might be causing the issue:\n")
        for path in result.file_paths:
            print("\t[+]"+path)
        related_code = fetch_code(result.grep_commands,os.getenv("PROJECT_PATH"))    
        return {
            "related_files": list(result.file_paths),
            "folder_structure":project_map,
            "grep_commands":result.grep_commands,
            "related_code":related_code,
            "code_fetch_attempts":state.code_fetch_attempts + 1,
            "status": "culprits_identified"
        }
    except Exception as e:
        print(f"Error in structured output: {e}")
        return {"status": "error_in_analysis"}
    