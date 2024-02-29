import unittest
from unittest.mock import patch, MagicMock
import mychangetest  # assuming verify.py is in the same directory

class TestVerifyFunctions(unittest.TestCase):

    @patch("verify.get_sender_info")
    @patch("verify.send_email")
    @patch("verify.insert_or_update_user_in_db")
    @patch("verify.generate_username")
    @patch("verify.generate_password")
    def test_generate_and_send_email_success(self, mock_generate_password, mock_generate_username,
                                             mock_insert_or_update_user_in_db, mock_send_email, mock_get_sender_info):
        # Mocking dependencies
        mock_generate_password.return_value = "mock_password"
        mock_generate_username.return_value = "mock_username"
        mock_get_sender_info.return_value = ("mock_sender_email", "mock_sender_password")

        mychangetest.root = MagicMock()

        # Execute the function
        mychangetest.generate_and_send_email()

        # Verify that the expected functions are called with the correct arguments
        mock_generate_username.assert_called_once()
        mock_generate_password.assert_called_once()
        mock_insert_or_update_user_in_db.assert_called_once_with("mock_receiver_email", "mock_username", "mock_password")
        mock_send_email.assert_called_once_with(mychangetest.root, "mock_receiver_email", "mock_username", "mock_password",
                                               "mock_sender_email", "mock_sender_password")

    @patch("verify.get_sender_info")
    @patch("verify.send_email")
    @patch("verify.insert_or_update_user_in_db")
    @patch("verify.generate_username")
    @patch("verify.generate_password")
    def test_generate_and_send_email_failure(self, mock_generate_password, mock_generate_username,
                                             mock_insert_or_update_user_in_db, mock_send_email, mock_get_sender_info):
        # Mocking dependencies
        mock_generate_password.return_value = "mock_password"
        mock_generate_username.return_value = "mock_username"
        mock_get_sender_info.return_value = None

        mychangetest.root = MagicMock()

        # Execute the function
        mychangetest.generate_and_send_email()

        # Verify that the expected functions are not called in case of failure
        mock_generate_username.assert_not_called()
        mock_generate_password.assert_not_called()
        mock_insert_or_update_user_in_db.assert_not_called()
        mock_send_email.assert_not_called()

    @patch("verify.get_sender_info")
    @patch("verify.showerror")
    def test_generate_and_send_email_exception_handling(self, mock_showerror, mock_get_sender_info):
        # Mocking dependencies
        mock_get_sender_info.side_effect = Exception("Some error")

        mychangetest.root = MagicMock()

        # Execute the function
        mychangetest.generate_and_send_email()

        # Verify that showerror is called with the correct arguments
        mock_showerror.assert_called_once_with("Error", "Failed to fetch sender information from database.", parent=verify.root)

   

if __name__ == "__main__":
    unittest.main()
