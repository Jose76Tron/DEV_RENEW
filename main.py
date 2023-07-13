import sys
import time
import random
import requests
from nacl import encoding, public


# Parameters
args = sys.argv[1:]
client_id = args[0]
client_secret = args[1]
refresh_token = args[2]
github_token = args[3]
github_repo = args[4]

# Graph API endpoints
calls = [
    'https://graph.microsoft.com/v1.0/me/drive/root',
    'https://graph.microsoft.com/v1.0/me/drive',
    'https://graph.microsoft.com/v1.0/drive/root',
    'https://graph.microsoft.com/v1.0/users',
    'https://graph.microsoft.com/v1.0/me/messages',
    'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
    'https://graph.microsoft.com/v1.0/me/drive/root/children',
    'https://api.powerbi.com/v1.0/myorg/apps',
    'https://graph.microsoft.com/v1.0/me/mailFolders',
    'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
    'https://graph.microsoft.com/v1.0/applications?$count=true',
    'https://graph.microsoft.com/v1.0/me/?$select=displayName,skills',
    'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
    'https://graph.microsoft.com/beta/me/outlook/masterCategories',
    'https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top=1',
    'https://graph.microsoft.com/v1.0/sites/root/lists',
    'https://graph.microsoft.com/v1.0/sites/root',
    'https://graph.microsoft.com/v1.0/sites/root/drives'
]

# Get the public key of the Github repo
def get_public_key():
    url = f"https://api.github.com/repos/{github_repo}/actions/secrets/public-key"
    headers = {
        "Authorization": f"token {github_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json() # Including key and key_id

# Encrypt the secret value using the public key
def encrypt(public_key, secret_value):
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return encoding.Base64Encoder().encode(encrypted).decode("utf-8")

# Update the secret
def update_secret(secret_name, secret_value):
    url = f"https://api.github.com/repos/{github_repo}/actions/secrets/{secret_name}"
    headers = {
        "Authorization": f"token {github_token}"
    }
    public_key = get_public_key()
    data = {
        "encrypted_value": encrypt(public_key["key"], secret_value),
        "key_id": public_key["key_id"]
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 204:
        print(f"GitHub {secret_name} secret updated successfully!")
    else:
        print(f"Failed to update GitHub {secret_name} secret. Status code: {response.status_code}")

# Get a new access token and refresh token
def get_access_token(refresh_token, client_id, client_secret):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    response = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    refresh_token = response.json()['refresh_token']
    return response.json()['access_token']

# Main run
def run():
    random.shuffle(calls)
    endpoints = calls[random.randint(0,10)::]
    access_token = get_access_token(refresh_token, client_id, client_secret)
    session = requests.Session()
    session.headers.update({
        'Authorization': access_token,
        'Content-Type': 'application/json'
    })
    num = 0
    for endpoint in endpoints:
        try:
            response = session.get(endpoint)
            if response.status_code == 200:
                num += 1
                print(f'{num}th Call successful')
        except requests.exceptions.RequestException as e:
            print(e)
            pass
    localtime = time.asctime(time.localtime(time.time()))
    print('The end of this run is :', localtime)
    print('Number of calls is :', str(len(endpoints)))

for _ in range(3):
    run()

# Update the value of the REFRESH_TOKEN secret by the last value of the refresh_token variable
update_secret("REFRESH_TOKEN", refresh_token)
