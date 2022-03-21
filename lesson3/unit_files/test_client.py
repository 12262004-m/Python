import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from client import create_presence, process_answer
from files.variables import PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, ACTION

class Test(unittest.TestCase):
    def test_def_create_presence(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: "Гость"}})

    def test_def_process_answer_200(self):
        self.assertEqual(process_answer({RESPONSE: 200}), "OK")

    def test_def_process_answer_400(self):
        self.assertEqual(process_answer({RESPONSE: 400, ERROR: "Ошибка"}), "Ошибка")

    def test_no_response(self):
        self.assertEqual(ValueError, process_answer, {ERROR: "Ошибка"})

if __name__ == '__main__':
    unittest.main()