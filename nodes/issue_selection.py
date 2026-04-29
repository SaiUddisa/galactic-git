import os

from state import State
from tools.list_issues import list_issues


def issue_selection_node(state:State):
    print("Good Day !! These are the issues available: \n")
    issues = list_issues(os.getenv("OWNER"), os.getenv("REPO"), os.getenv("GITHUB_TOKEN"))

    for index,issue in enumerate(issues,start=1):
        print(f'   {index}. {issue['title']}')
        
    user_choice=int(input("\nPlease choose the issue you want to fix: "))

    selected_issue = user_choice-1

    print(f"Great!! let fix this issue \n\n    Title: {issues[selected_issue]['title']}\n")
    print(f"    Description:\n \t{issues[selected_issue]['body']}\n")
    return {
            "issue_title": issues[selected_issue]['title'],
            "issue_description": issues[selected_issue]['body'],
            "status": "issue_selection" 
        }