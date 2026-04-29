import json
import os
import requests
from state import State
from tools.apply_changes import apply_changes


def fix_and_push(state :State):
    apply_changes(state.sed_commands,os.getenv("PROJECT_PATH"),state.branch_name,state.commit_message)
   

    
    
           