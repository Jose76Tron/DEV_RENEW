# **MS-E5-Dev-Auto-Renew**

This repo is forked from [https://github.com/kylierst/MSO_E5_Dev_AutoRenew](https://github.com/kylierst/MSO_E5_Dev_AutoRenew).

MS-E5-Dev-Auto-Renew is a Python application based on Git Actions that uses Microsoft Graph API to activate Microsoft Office 365 E5 Developer Trail membership auto-renewal automatically. This guide will provide you with easy-to-understand steps for setting up and running the application.

## **Prerequisites**

- A GitHub account
- An existing or new Microsoft Developer E5 account with trial Subscription
- An Azure Portal account
- Basic knowledge of GitHub, Python, and Azure Portal

## **Setup Instructions (Encrypted Secure Version)**

### **Setup MS App**

The goal of this step is to get the client ID, the client secret, and the refresh token.

1. Register a new application in Azure Active Directory
    - Select "Accounts in any organizational directory (Any Azure AD directory - Multitenant)", remember **Multitenant**.
    - Select "Web" for the redirect URL, and enter "**[http://localhost:53682/](http://localhost:53682/)**" for the redirect URL.
    - Click "Client credentials" and then create client secret.
    - Now you have the client ID and the client secret, save them to a text file.
2. Set application permissions
    - Select the following permissions: **`files.read.all`**, **`files.readwrite.all`**, **`sites.read.all`**, **`sites.readwrite.all`**, **`user.read.all`**, **`user.readwrite.all`**, **`directory.read.all`**, **`directory.readwrite.all`**, **`mail.read`**, **`mail.readwrite`**, **`mailboxsetting.read`**, and **`mailboxsetting.readwrite`**.
    - Grant permission for all selected above permissions.
3. Get refresh token
    - Install rclone on your machine that can open a browser (not on a headless machine).
    - Open terminal and run command **`rclone authorize "onedrive" "client_id" "client_secret"`** with **client_id** and **client_secret** you get in the first step.
    - Copy the refresh token value from the terminal result (if you are patient enough) or install a Chrome extention called JsonHandle to get it.
    - Save the refresh token to the text file above.

### **Setup your Github account**

1. Fork the MS-E5-Dev-Auto-Renew repository to your GitHub account
2. Generate a personal access token
    - Click your avatar at the top right corner > Settings > Developer settings > Personal access tokens > Tokens (classic) > Generate new token.
    - Set the name to anything you like.
    - Check the options **`repo`**, **`admin:repo_hook`**, and **`workflow`**.
    - Click **Generate token** button.
    - Save the generated token to the text file above.
3. Setup repo secrets
    - On your repo's homepage, click Settings > Secrets and Variables > Actions (Repo settings not Github account settings).
    - Click **New repository secrets** button and create 4 secrets with the value as given below:
        - Name: **`CONFIG_ID`** - Value: the client ID in the text file
        - Name: **`CONFIG_KEY`** - Value: the client secret in the text file
        - Name: **`REFRESH_TOKEN`** - Value: the refresh token in the text file
        - Name: **`GH_TOKEN`** - Value: the personal access token in the text file
4. Setup workflow permissions
    - On your repo's homepage, click Settings > Actions > General.
    - In the **Workflow permissions** section, select **Read and write permissions** option.

### **Manually call the workflow**

There are two ways to call the workflow manually:
1. On your repo's homepage, click the star button (above the repo's description section).
2. Click your repo's Actions tab > Click your workflow name > Click **Run workflow** dropdown > Click **Run workflow** button.

## **Additional Information**

- Click the repo's Actions tab to see the log of the workflow and check if the API is called correctly or if there are any errors.
- The default setting is to run three rounds every two hours. You can modify your own crontab to change the frequency and time.
- If you need to modify the API calls, you can check the Graph Explorer at **[https://developer.microsoft.com/graph/graph-explorer/preview](https://developer.microsoft.com/graph/graph-explorer/preview)**.
- The GitHub Action provides a virtual environment with 2-core CPU, 7 GB RAM memory, and 14 GB SSD hard disk space.
- Each repository can only support 20 concurrent calls.
