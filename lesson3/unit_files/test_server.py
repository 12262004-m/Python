import unittest
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from lesson3.files.variables import ACTION, ACCOUNT_NAME, ERROR, PRESENCE, TIME, USER, RESPONSE
from lesson3.server import client_message

class Test(unittest.TestCase):
    error_dict = {
        RESPONSE: 400,
        ERROR: "Ошибка"
    }
    correct_dict = {
        RESPONSE: 200
    }

    def test_correct_request(self):
        self.assertEqual(client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: "Гость"}}), self.correct_dict)

    def test_no_action(self):
        self.assertEqual(client_message({TIME: 1.1, USER: {ACCOUNT_NAME: "Гость"}}), self.error_dict)

    def test_wrong_action(self):
        self.assertEqual(client_message({ACTION: "Wrong", TIME: 1.1, USER: {ACCOUNT_NAME: "Гость"}}), self.error_dict)

    def test_no_time(self):
        self.assertEqual(client_message({ACTION: PRESENCE, USER: {ACCOUNT_NAME: "Гость"}}), self.error_dict)

    def test_no_user(self):
        self.assertEqual(client_message({ACTION: PRESENCE, TIME: 1.1}), self.error_dict)

    def test_unknown_user(self):
        self.assertEqual(client_message({ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: "Гость1"}}), self.error_dict)


if __name__ == '__main__':
    unittest.main()