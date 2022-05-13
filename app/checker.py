#!/usr/bin/env python3
from time import sleep
from core import emailutils, credentials, notification

DEBUG = True

def main():
    cred = credentials.Credentials()
    limit = int(cred.read_file('DEFAULT', 'limit'))
    interval = int(cred.read_file('DEFAULT', 'interval'))
    if cred.read_file('CRED', 'user') == 'no':
        cred.create_credentials()
    checker = emailutils.MissionControl(
            cred.read_file('CRED', 'user'),
            cred.read_file('CRED', 'pass'),
            cred,
            limit
        )
    # UI start
    sleep(30)
    while 1:
        checker.read_email()
        notification.Notification.send_notification(checker.new_emails)
        if DEBUG:
            break
        sleep(interval)

if __name__ == "__main__":
    main()