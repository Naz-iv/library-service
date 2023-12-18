from unittest.mock import Mock, patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from notifications_service.models import TelegramUser
from borrowing_service.models import Borrowing
from notification_service.bot_commands import (is_user,
                                               welcome_message,
                                               help_information,
                                               user_borrowings)


class NotificationServiceTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client = APIClient()
        self.refresh_token = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh_token.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_is_user(self):
        message = Mock()
        message.text = 'test@example.com'

        self.assertFalse(is_user(message))

        TelegramUser.objects.create(user_id=self.user, chat_id=12345)

        self.assertTrue(is_user(message))

    def test_welcome_message(self):
        message = Mock()
        message.from_user.full_name = 'Test User'

        with patch('notification_service.bot.reply_to') as mock_reply:
            welcome_message(Mock(), message)

        mock_reply.assert_called_with(
            message,
            "Hello, Test User!\nWelcome to the Library Service!\n/help for more information"
        )

    def test_help_information(self):
        message = Mock()

        with patch('notification_service.bot.reply_to') as mock_reply:
            help_information(Mock(), message)

        mock_reply.assert_called_with(
            message,
            "/start - start bot\n/help - show information about commands\n/my_borrowings - show all your borrowings\n"
        )

    def test_user_borrowings(self):
        message = Mock()
        message.chat.id = 12345

        Borrowing.objects.create(
            user=self.user.customer,
            book='Test Book',
            borrow_date='2023-01-01',
            expected_return_date='2023-02-01',
            is_active=True
        )

        with patch('notification_service.bot.reply_to') as mock_reply:
            user_borrowings(Mock(), message)

        mock_reply.assert_called_with(
            message,
            "Your borrowings:\n\n-Book:  Test Book\n--Borrow date:  2023-01-01\n--Expected return date:  2023-02-01\n"
        )
