import imaplib
import email
from collections import namedtuple


Message = namedtuple("Message", "title body")


class MissionControl:
    """Read email and notify if is the case
    """
    def __init__(self, username: str, password: str, cred, limit: int=10) -> None:
        self.email = imaplib.IMAP4_SSL('imap.gmail.com')
        self.email.login(username, password)
        self.limit = limit
        self.config = cred

    def to_timestamp(self, date_message):
        msg_datetime = email.utils.parsedate_to_datetime(date_message)
        return msg_datetime.timestamp()
    
    def save_timestamp(self, message):
        """Extract timestamp and save it
        """
        t_stamp = self.to_timestamp(message['date'])
        self.config.create_timestamp_check_point(t_stamp)
    
    def read_email(self):
        latest_timestamp = float(self.config.read_file('APP', 'timestamp'))
        _, msgs = self.email.select('INBOX')
        latest_message = None
        for i in range(int(msgs[0]), int(msgs[0]) - self.limit, -1):
            _, message = self.email.fetch(str(i), '(RFC822)')
            for r in message:
                if isinstance(r, tuple):
                    message = email.message_from_bytes(r[1])
                    if latest_message is None:
                        latest_message = message
                    current_timestamp = self.to_timestamp(message['date'])
                    if current_timestamp <= latest_timestamp:
                        continue
                    subject = email.header.decode_header(message["subject"])
                    e_from = email.header.decode_header(message["from"])
                    codification = subject[0][1]
                    if isinstance(subject[0][0], str):
                        print(subject[0][0])
                    else: 
                        print(subject[0][0].decode('utf-8' if codification is None else codification))
                    
                    codification = e_from[0][1]
                    if isinstance(e_from[0][0], str):
                        print (e_from[0][0])
                    else:
                        print(e_from[0][0].decode('utf-8' if codification is None else codification))
                    print('===================================')
        self.save_timestamp(latest_message)