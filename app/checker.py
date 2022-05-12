from core import emailutils, credentials

def main():
    cred = credentials.Credentials()
    limit = int(cred.read_file('DEFAULT', 'limit'))
    
    if cred.read_file('CRED', 'user') == 'no':
        cred.create_credentials()
    checker = emailutils.MissionControl(
        cred.read_file('CRED', 'user'),
        cred.read_file('CRED', 'pass'),
        cred,
        limit
    )
    checker.read_email()

if __name__ == "__main__":
    main()