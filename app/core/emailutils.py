import imaplib
import email
from collections import namedtuple


Message = namedtuple("Message", "title body")


class MissionControl:
    """Read email and notify if is the case
    """
    def __init__(self, username: str, password: str, config, mark_as_read: bool, limit: int=10) -> None:
        self.email = imaplib.IMAP4_SSL('imap.gmail.com')
        self.email.login(username, password)
        self.limit = limit
        self.config = config
        self.mark_as_read = mark_as_read
        self._new_emails = []

    @property
    def new_emails(self):
        return self._new_emails
    
    def _to_timestamp(self, date_message):
        msg_datetime = email.utils.parsedate_to_datetime(date_message)
        return msg_datetime.timestamp()
    
    def _save_timestamp(self, message):
        """Extract timestamp and save it
        """
        t_stamp = self._to_timestamp(message['date'])
        self.config.create_timestamp_check_point(t_stamp)

    def _mark_as_unseen(self, message_uid: str) -> None:
        """After notify, mark as unseen to not modify the
        usual bahaviour

        Args:
            message_id (str): message uid
        """
        self.email.uid('STORE', message_uid, '-FLAGS', '(\Seen)')
    
    def read_email(self):
        self._new_emails = []
        latest_timestamp = float(self.config.read_file('APP', 'timestamp'))
        _, msgs = self.email.select('INBOX', readonly=False)
        latest_message = None
        for i in range(int(msgs[0]), int(msgs[0]) - self.limit, -1):
            _, message = self.email.fetch(str(i), '(RFC822)')
            for r in message:
                email_subject = ''
                email_from = ''
                if isinstance(r, tuple):
                    message = email.message_from_bytes(r[1])
                    if latest_message is None:
                        latest_message = message
                    current_timestamp = self._to_timestamp(message['date'])
                    if current_timestamp <= latest_timestamp:
                        continue
                    subject = email.header.decode_header(message["subject"])
                    e_from = email.header.decode_header(message["from"])
                    codification = subject[0][1]
                    if isinstance(subject[0][0], str):
                        email_subject = subject[0][0]
                    else: 
                        email_subject = subject[0][0].decode('utf-8' if codification is None else codification)
                    
                    codification = e_from[0][1]
                    if isinstance(e_from[0][0], str):
                        email_from = e_from[0][0]
                    else:
                        email_from = e_from[0][0].decode('utf-8' if codification is None else codification)
                    self._new_emails.append(Message(email_from, email_subject))
            
            # Nothing happen!
            if not self.mark_as_read:
                self._mark_as_unseen(str(i))
    
        self._save_timestamp(latest_message)