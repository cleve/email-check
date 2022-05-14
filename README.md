# email-check
Lightweight email checker for Gmail.

# Use
Launch the app and complete the info requested. The first time you will be 
ask by credentials.

Gmail use app password for external use, you need to generate it.

To launch

```sh
cd app
python3 checker.py
```

# Configuration

There is a config file located in **data/config.ini**

```sh
[DEFAULT]
# Interval to check new emails
interval = 300

# Max amount of emails to check
limit = 10

# Once the email is checked, mark as reas or not
markasread = True

# Credentials
[CRED]
user = mauricio.cleveland@gmail.com
pass = fkfvoaerjovyfgva

# Use by the app
[APP]
timestamp = 0
```