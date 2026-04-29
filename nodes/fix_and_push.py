import os
import subprocess

from pydantic import json
import requests
from state import State

from tools.apply_changes import apply_changes


def fix_and_push(state :State):
    apply_changes(state.sed_commands,os.getenv("PROJECT_PATH"),state.branch_name,state.commit_message)
    #raiseing an MR
    # Configuration
    OWNER = os.getenv("OWNER")
    REPO = os.getenv("REPO")
    TOKEN = os.getenv("GITHUB_TOKEN")

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    data = {
        "title":state.issue_title ,
        "body": state.commit_message,
        "head": state.branch_name,  
        "base": "master"                  
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Check if successful (201 Created)
        if response.status_status == 201:
            print("Pull Request created successfully!")
            print(f"PR URL: {response.json().get('html_url')}")
        else:
            print(f"Failed to create PR: {response.status_code}")
            print(response.json())
        return    
    except Exception as e:
        print(f"An error occurred: {e}")

    
    
           