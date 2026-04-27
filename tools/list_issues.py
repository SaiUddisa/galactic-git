import requests

def list_issues(owner, repo, token):
   
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    params = {
        "state": "open",
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    issues = response.json()
    
    
    return [issue for issue in issues if "pull_request" not in issue]

