import sys
import os

#import the path of the Bot directory
dirname = os.path.dirname(__file__)
print(dirname)
path = dirname[:len(dirname) - 5]
sys.path.insert(0, path)

import unittest
from Bot.poll import Poll, AnswerOption, PollError


class TestAnswerOption(unittest.TestCase):

    def test___init__(self):
        self.assertEqual(AnswerOption("string").votes, 0)
        self.assertEqual(AnswerOption("string").name, "string")

    def test___str__(self):
        self.assertEqual(str(AnswerOption("string")), "string")

class TestPoll(unittest.TestCase):

    def test___init__(self):

        #default func call
        obj1 = Poll(None)
        self.assertEqual(obj1.poll_name, "default")
        self.assertEqual(obj1.time, 60)
        self.assertEqual(obj1.ans_number, 0)
        self.assertEqual(obj1.answer_options, [])
        self.assertEqual(obj1.mess, None)
        self.assertEqual(obj1.emojis, ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"])
        self.assertEqual(obj1.channel, None)

        obj1 = Poll(None, 5, 44, "Testname")
        self.assertEqual(obj1.ans_number, 5)
        self.assertEqual(obj1.time, 44)
        self.assertEqual(len(obj1.answer_options), 5)
        self.assertEqual(obj1.answer_options[4].name, "default_option 4")
        self.assertEqual(obj1.poll_name, "Testname")
        
        try:
            Poll(None, 12)
            self.fail("PollError should be raised here")
        except PollError as e:
            self.assertEqual(e.error_message,"Maximum of 11 answers per Poll are allowed")
        
        try:
            Poll(None, -4)
            self.fail("PollError should be raised here")
        except PollError as e:
            self.assertEqual(e.error_message,"ans_number must be positive! (ans_number was -4)")

    def test_add_answer(self):
        
        obj = Poll(None)
        obj.add_answer("test0")
        obj.add_answer("test1")
        obj.add_answer("test2")
        self.assertEqual(obj.ans_number, 3)
        self.assertEqual(obj.ans_number, len(obj.answer_options))
        for i in range(len(obj.answer_options)):
            self.assertEqual(obj.answer_options[i].name, "test" + str(i))
        for i in obj.answer_options:
            self.assertEqual(i.votes, 0)
        try:
            obj.add_answer("these_are_more_than_30_characters")
            self.fail("PollError should be raised here")
        except PollError as e:
            self.assertEqual(e.error_message, "Could not add answer 'these_are_more_than_30_characters'. Maximum of 30 Charactes are allowed.")

        obj = Poll(None, 11)
        try:
            obj.add_answer("test")
            self.fail("PollError should be raised here")
        except PollError as e:
            self.assertEqual(e.error_message, "Could not add answer 'test'. Maximum number of answer options reached.")


    def test_delete_answer(self):
        obj = Poll(None, 6)
        ans = obj.delete_answer(1)
        self.assertEqual(obj.ans_number, 5)
        self.assertEqual(ans.name, "default_option 1")
        try:
            obj.delete_answer(5)
            self.fail("PollError should be raised here")
        except PollError as e:
            self.assertEqual(str(e), "Answer could not be deleted (doesn't exist)")

if __name__ == '__main__':
    unittest.main()