

# SSH key

If using an unusual file name for public/private key with git, create a files as follows:

In `~/.ssh/config`, add:

```
host github.com
 HostName github.com
 IdentityFile ~/.ssh/id_rsa_github
 User git
 ```

 # Virtual Environments

 The venv module tends to fail when creating a virtual environment for me. Don't totally know why.  For example:

```
python -m venv foobar
Error: Command '['C:\\trash\\foobar\\Scripts\\python.exe', '-Im', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1.
```

Workaround:
```
python -m venv --without-pip foobar
# Manually install pip
curl https://bootstrap.pypa.io/get-pip.py | python
```
