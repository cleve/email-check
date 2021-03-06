import subprocess

class Notification:
    @staticmethod
    def send_notification(messages: list) -> None:
        if len(messages) == 1:
            for message in messages:
                subprocess.call(
                    [
                        'notify-send',
                        f'New e-mail from {message.title}',
                        message.body,
                        '-t', '30000'
                    ])
        else:
            subprocess.call(['notify-send', 'New emails', '-t', '30000'])

        