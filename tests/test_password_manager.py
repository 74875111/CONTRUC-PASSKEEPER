import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Añadir la ruta del directorio app al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

import password_manager as pm

class TestPasswordManager(unittest.TestCase):

    @patch('password_manager.load_passwords')
    def test_view_password_no_passwords(self, mock_load_passwords):
        mock_load_passwords.return_value = {}
        localization = MagicMock()
        localization.translate.side_effect = lambda x: x

        with patch('builtins.input', return_value=''):
            with patch('builtins.print') as mock_print:
                pm.view_password('session1', localization, 'folder1')
                mock_print.assert_any_call('no_passwords_saved')

    @patch('password_manager.load_passwords')
    def test_view_password_no_entries_in_folder(self, mock_load_passwords):
        mock_load_passwords.return_value = {'session1': {'folders': {}}}
        localization = MagicMock()
        localization.translate.side_effect = lambda x: x

        with patch('builtins.input', return_value=''):
            with patch('builtins.print') as mock_print:
                pm.view_password('session1', localization, 'folder1')
                mock_print.assert_any_call('no_passwords_saved')

    @patch('password_manager.load_passwords')
    @patch('password_manager.cipher.decrypt')
    def test_view_password_success(self, mock_decrypt, mock_load_passwords):
        mock_load_passwords.return_value = {
            'session1': {
                'folders': {
                    'folder1': [
                        {'id': '1', 'name': 'example', 'username': 'user', 'password': 'encrypted_password'}
                    ]
                }
            }
        }
        mock_decrypt.return_value = 'decrypted_password'
        localization = MagicMock()
        localization.translate.side_effect = lambda x: x

        with patch('builtins.input', return_value='1'):
            with patch('builtins.print') as mock_print:
                pm.view_password('session1', localization, 'folder1')
                mock_print.assert_any_call('password: decrypted_password')

    @patch('password_manager.load_passwords')
    def test_view_password_invalid_option(self, mock_load_passwords):
        mock_load_passwords.return_value = {
            'session1': {
                'folders': {
                    'folder1': [
                        {'id': '1', 'name': 'example', 'username': 'user', 'password': 'encrypted_password'}
                    ]
                }
            }
        }
        localization = MagicMock()
        localization.translate.side_effect = lambda x: x

        with patch('builtins.input', return_value='invalid'):
            with patch('builtins.print') as mock_print:
                pm.view_password('session1', localization, 'folder1')
                mock_print.assert_any_call('invalid_option')

if __name__ == '__main__':
    unittest.main()