import subprocess

class Notification:
    @staticmethod
    def send_notification(messages: list) -> None:
        if len(messages) <= 3:
            for message in messages:
                subprocess.call(['notify-send', message])
        else:
            subprocess.call(['notify-send', "New email", "You have new emails"])

        