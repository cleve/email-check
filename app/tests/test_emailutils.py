import unittest
from unittest.mock import patch, MagicMock
from core import emailutils, notification

class TestEmailUtils(unittest.TestCase):

    @patch('core.configuration.Configuration')
    @patch('imaplib.IMAP4_SSL')
    def setUp(self, mock_imaplib, mock_config) -> None:
        self.email = emailutils.MissionControl('no', 'no', mock_config, True)
        return super().setUp()


    def test_initial_state(self):
        assert self.email.mark_as_read
        assert len(self.email.new_emails) == 0

    @patch('subprocess.call')
    def test_notification_generic(self, mock_subprocess):
        notification_object = notification.Notification()
        m1 = emailutils.Message('title 1', 'body 1')
        m2 = emailutils.Message('title 2', 'body 2')
        notification_object.send_notification([m1, m2])

        args = mock_subprocess.call_args_list[0][0][0]
        self.assertListEqual(
            ['notify-send', 'New emails', '-t', '30000'], args)

    @patch('subprocess.call')
    def test_notification_one_email(self, mock_subprocess):
        notification_object = notification.Notification()
        m1 = emailutils.Message('title 1', 'body 1')
        notification_object.send_notification([m1])

        args = mock_subprocess.call_args_list[0][0][0]
        self.assertListEqual(
            ['notify-send', 'New e-mail from title 1', 'body 1', '-t', '30000'], args)
