#!/usr/bin/env python3
from time import sleep
from core import configuration, emailutils, notification


DEBUG = True

def main():
    config = configuration.Configuration()
    interval = int(config.read_file('DEFAULT', 'interval'))
    mark_as_read = config.read_file('DEFAULT', 'markasread')
    if config.read_file('CRED', 'user') == 'no':
        config.create_credentials()
    checker = emailutils.MissionControl(
            config.read_file('CRED', 'user'),
            config.read_file('CRED', 'pass'),
            config,
            mark_as_read
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