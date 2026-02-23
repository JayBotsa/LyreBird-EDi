import requests
import json

# Your GitHub token
token = 'your_github_token_here'  # Replace with actual

# Headers for auth
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Repo details
repo_name = 'Pure-Reflection-EDi'  # Or your choice
repo_desc = 'EDi unveiling: conceptual core, pilots, resonance-refresh framework. Farmers first, Mars next.'
is_private = True

# Payload
payload = {
    'name': repo_name,
    'description': repo_desc,
    'private': is_private,
    'auto_init': True,  # Creates README
    'gitignore_template': 'Python'  # Optional
}

# Create repo
response = requests.post('https://api.github.com/user/repos', headers=headers, data=json.dumps(payload))

if response.status_code == 201:
    print(f"Repo created: {response.json()['html_url']}")
else:
    print(f"Error: {response.json()}")
