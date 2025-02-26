reminders to self:

Combines git add and git commit:
    git commit -am 'message' 

Push to remote repo:
    git push -u origin main
    or just 
    git push
    
Setting up my git to have my token for login to repo: run these 2 commands (replace <blah_blah> with relevant info):
    git config --global credential.helper store
    git config --global url."https://<your_github_username>:<your_token>@github.com/".insteadOf "https://github.com/"