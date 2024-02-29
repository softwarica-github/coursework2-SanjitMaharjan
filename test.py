import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import main  # assuming main.py is in the same directory

class TestMainFunctions(unittest.TestCase):

    @patch("main.connect_to_database")
    def test_check_credentials_valid(self, mock_connect_to_database):
        # Mocking database connection
        mock_connection = MagicMock()
        mock_connect_to_database.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("some_data",)]

        result = main.check_credentials("username", "password")

        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()

    @patch("main.connect_to_database")
    def test_check_credentials_invalid(self, mock_connect_to_database):
        # Mocking database connection
        mock_connection = MagicMock()
        mock_connect_to_database.return_value = mock_connection
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        result = main.check_credentials("invalid_username", "invalid_password")

        self.assertFalse(result)
        mock_cursor.execute.assert_called_once()

    @patch("main.check_account")
    @patch("main.threading.Thread")
    def test_start_checking(self, mock_thread, mock_check_account):
        # Mocking thread and check_account function
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        accounts = ["user1:pass1", "user2:pass2"]
        gui_output = MagicMock()
        max_threads = 2

        main.start_checking(accounts, gui_output, max_threads)

        # Ensure that the correct number of threads are created and started
        self.assertEqual(mock_thread.call_count, len(accounts))
        mock_thread_instance.start.assert_called()

   
if __name__ == "__main__":
    unittest.main()
