import os
import sys
import time
import json
import requests
import shutil
from nacl import encoding, public


class MSTokens():
    def __init__(self, mode="pro", client_id=None, client_secret=None, refresh_token=None, github_token=None, github_repo=None, tokens_file_name=None):
        self.app_folder = os.path.dirname(os.path.realpath(__file__))
        self.mode = mode
        self.client_id = client_id
        self.client_secret = client_secret
        if mode == "pro" and refresh_token is not None and github_token is not None and github_repo is not None:
            self.refresh_token = refresh_token
            self.github_token = github_token
            self.github_repo = github_repo
        elif mode == "dev" and tokens_file_name is not None:
            self.tokens_file_name = tokens_file_name
            self.tokens_file_path = os.path.join(self.app_folder, self.tokens_file_name)
            self.refresh_token = self.get_refresh_token_from_file()
        else:
            print("Error: Wrong parameters for MSTokens class")
            sys.exit()

    # Get the public key of the Github repo
    def get_public_key(self):
        url = f"https://api.github.com/repos/{self.github_repo}/actions/secrets/public-key"
        headers = {
            "Authorization": f"token {self.github_token}"
        }
        response = requests.get(url, headers=headers)
        return response.json() # Including key and key_id

    # Encrypt the secret value using the public key
    def encrypt(self, public_key, secret_value):
        public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return encoding.Base64Encoder().encode(encrypted).decode("utf-8")

    # Update the secret
    def update_secret(self, secret_name, secret_value):
        url = f"https://api.github.com/repos/{self.github_repo}/actions/secrets/{secret_name}"
        headers = {
            "Authorization": f"token {self.github_token}"
        }
        public_key = self.get_public_key()
        data = {
            "encrypted_value": self.encrypt(public_key["key"], secret_value),
            "key_id": public_key["key_id"]
        }
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 204:
            print("{}: {} {}".format("Success", "Update GitHub secret", secret_name))
        else:
            print("{}: {} {} {} {}".format("Error", "Update GitHub secret", secret_name, response.status_code, response.text))

    # Get a new access token and refresh token
    def get_access_token(self):
        url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": "http://localhost:53682/"
        }
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            print("{}: {}".format("Success", "Get access token"))
            if self.mode == "pro":
                self.update_secret("REFRESH_TOKEN", response.json()["refresh_token"])
            elif self.mode == "dev":
                self.save_tokens_to_file(json.dumps(response.json())) # Save data into file
            return response.json()["access_token"]
        else:
            print("{}: {} {} {}".format("Error", "Get access token", response.status_code, response.text))

    # Get refresh token from file
    def get_refresh_token_from_file(self):
        with open(self.tokens_file_path, "r") as file:
            data = file.read()
        return json.loads(data)["refresh_token"]
    
    # Save the new access token and refresh token into file
    def save_tokens_to_file(self, data):
        # Create a backup
        tokens_backup_file_path = os.path.join(self.app_folder, self.tokens_file_name[:-4] + "-" + str(int(time.time())) + ".txt")
        shutil.copy2(self.tokens_file_path, tokens_backup_file_path)
        # Try to write new contents into file
        try:
            with open(self.tokens_file_path, "w") as file:
                file.write(data)
            # Delete backup if write new contents successfully
            os.remove(tokens_backup_file_path)
        except:
            # Restore the previous contents if failed to write new contents
            shutil.copy2(tokens_backup_file_path, self.tokens_file_path)


if __name__ == "__main__":
    # For production
    mst = MSTokens(
        mode="pro",
        client_id=sys.argv[1],
        client_secret=sys.argv[2],
        refresh_token=sys.argv[3],
        github_token=sys.argv[4],
        github_repo=sys.argv[5]
    )
    print(mst.get_access_token())

    # For testing on local machine
    # mst = MSTokens(
    #     mode="dev",
    #     client_id="", # Manually enter
    #     client_secret="", # Manually enter
    #     tokens_file_name="tokens.txt" # The refresh token is in this file
    # )
    # print(mst.get_access_token())
