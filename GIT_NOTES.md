

# SSH key

If using an unusual file name for public/private key with git, create a files as follows:

In `~/.ssh/config`, add:

```
host github.com
 HostName github.com
 IdentityFile ~/.ssh/id_rsa_github
 User git
 ```
