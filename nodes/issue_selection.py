import os

from state import State
from tools.list_issues import list_issues


def issue_selection_node(state:State):
    print("Hai! These are the issues available: ")
    issues = list_issues("saiuddisa", "vue-videoplayer", os.getenv("GITHUB_TOKEN"))

    for index,issue in enumerate(issues,start=1):
        print(f'{index}. {issue['title']}')
        
    user_choice=int(input("please choose the issue you want to fix: "))

    selected_issue = user_choice-1

    print(f"Great!! let fix this issue\n Title: {issues[selected_issue]['title']}")
    print(f"Description: \n {issues[selected_issue]['body']}")
    return {
            "issue_title": issues[selected_issue]['title'],
            "issue_description": issues[selected_issue]['body'],
            "status": "issue_selection" 
        }