# PDF To Text tool that uses your email as a source
## How to get the client_secret.json ? 
Go to the Google Developers Console. 
Create a new project by clicking on the "Select a Project" dropdown at the top of the page and then clicking on the "New Project" button.
Give the project a name and click on the "Create" button.
In the left sidebar, click on "APIs & Services" and then click on "OAuth consent screen".
Choose the "External" user type and click on the "Create" button.
Enter a name for the application, add your email address, and click on the "Save" button.
In the left sidebar, click on "Credentials" and then click on the "Create Credentials" button and select "OAuth client ID".
Choose "Desktop app" as the application type, give it a name, and click on the "Create" button.
In the "OAuth client ID" page, click on the "Download" button to download the client_secret.json file.
Save the client_secret.json file in the same directory as your Python script.
Run the following script to authorize your application and get the token.json file:

