import string
import unittest
from unittest.mock import patch, MagicMock
import mytwofa  
class TestYourScript(unittest.TestCase):
    def test_generate_username(self):
        username = mytwofa.generate_username()
        self.assertEqual(len(username), 8)
        self.assertTrue(username.isalnum()) 

    def test_generate_password(self):
        password = mytwofa.generate_password()
        self.assertEqual(len(password), 12)
        self.assertTrue(any(char.islower() for char in password))
        self.assertTrue(any(char.isupper() for char in password))
        self.assertTrue(any(char.isdigit() for char in password))
        self.assertTrue(any(char in string.punctuation for char in password))

    @patch('mysql.connector.connect')
    def test_get_sender_info(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("test@example.com", "password123")
        mock_connect.return_value.cursor.return_value = mock_cursor
        sender_info = mytwofa.get_sender_info()
        self.assertEqual(sender_info, ("test@example.com", "password123"))

    @patch('mysql.connector.connect')
    def test_insert_or_update_user_in_db(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        mytwofa.insert_or_update_user_in_db("user@example.com", "username", "password123")
        
        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_connect.return_value.commit.called)

   
if __name__ == '__main__':
    unittest.main()
