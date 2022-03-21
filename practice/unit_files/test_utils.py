import unittest
import sys
import os
import json
sys.path.append(os.path.join(os.getcwd(), '..'))
from files.variables import ENCODING, ACTION, ACCOUNT_NAME, ERROR, PRESENCE, TIME, USER, RESPONSE
from files.utils import send_message, get_message

class TestSocket(unittest.TestCase):
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.recieved_message = None

    def recieve(self):
        js_test_message = json.dumps(self.test_dict)
        return js_test_message.encode(ENCODING)

    def send(self, message):
        js_test_message = json.dumps(self.test_dict)
        self.encoded_message = js_test_message.encode(ENCODING)
        self.recieved_message = message

class Test(unittest.TestCase):
    send_dict = {
        ACTION: PRESENCE,
        TIME: 1.1,
        USER: {ACCOUNT_NAME: "Test"}
    }
    recieve_error_dict = {
        RESPONSE: 400,
        ERROR: "Ошибка"
    }
    recieve_correct_dict = {
        RESPONSE: 200
    }

    def test_get_message(self):
        test_correct_socket = TestSocket(self.recieve_correct_dict)
        test_error_socket = TestSocket(self.recieve_error_dict)
        self.assertEqual(get_message(test_correct_socket), self.recieve_correct_dict)
        self.assertEqual(get_message(test_error_socket), self.recieve_error_dict)

    def test_send_message(self):
        test_socket = TestSocket(self.send_dict)
        send_message(test_socket, self.send_dict)
        self.assertEqual(test_socket.encoded_message, test_socket.recieved_message)
        self.assertRaises(TypeError, send_message, test_socket, "wrong dict")

if __name__ == '__main__':
    unittest.main()