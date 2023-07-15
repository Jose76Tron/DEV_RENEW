import sys
import time
import random
from helpers import *


class CallApis():
    def __init__(self, access_token=""):
        self.access_token = access_token
        self.endpoints = [
            "https://graph.microsoft.com/v1.0/me/drive/root",
            "https://graph.microsoft.com/v1.0/me/drive",
            "https://graph.microsoft.com/v1.0/drive/root",
            "https://graph.microsoft.com/v1.0/users",
            "https://graph.microsoft.com/v1.0/me/messages",
            "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules",
            "https://graph.microsoft.com/v1.0/me/drive/root/children",
            "https://api.powerbi.com/v1.0/myorg/apps",
            "https://graph.microsoft.com/v1.0/me/mailFolders",
            "https://graph.microsoft.com/v1.0/me/outlook/masterCategories",
            "https://graph.microsoft.com/v1.0/applications?$count=true",
            "https://graph.microsoft.com/v1.0/me/?$select=displayName,skills",
            "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta",
            "https://graph.microsoft.com/beta/me/outlook/masterCategories",
            "https://graph.microsoft.com/beta/me/messages?$select=internetMessageHeaders&$top=1",
            "https://graph.microsoft.com/v1.0/sites/root/lists",
            "https://graph.microsoft.com/v1.0/sites/root",
            "https://graph.microsoft.com/v1.0/sites/root/drives"
        ]

    # Main run
    def run(self):
        for _ in range(random.randint(3, 5)):
            random.shuffle(self.endpoints)
            endpoints = self.endpoints[random.randint(0, 10)::]
            num = 0
            for endpoint in endpoints:
                response = call_api_get("https://graph.microsoft.com/v1.0/users", self.access_token)
                if response.status_code == 200:
                    num += 1
                    print("{}: {} {}".format("Success", "Call API", endpoint))
                else:
                    print("{}: {} {} {} {}".format("Error", "Call API", endpoint, response.status_code, response.text))
            print("Successful calls: {}/{}".format(num, len(endpoints)))
            print("Finished at: {}\n".format(time.asctime(time.localtime(time.time()))))


if __name__ == "__main__":
    # For production
    call_api = CallApis(access_token=sys.argv[1])
    call_api.run()

    # For testing on local machine
    # from ms_tokens import MSTokens
    # mst = MSTokens(
    #     mode="dev",
    #     client_id="", # Manually enter
    #     client_secret="", # Manually enter
    #     tokens_file_name="tokens.txt" # The refresh token is in this file
    # )
    # call_api = CallApis(access_token=mst.get_access_token())
    # call_api.run()
