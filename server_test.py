#! /usr/bin/env python3
import unittest
from server import *

server = Server(["127.0.0.1", "192.168.1.1", "127.0.0.1", "37.98.5.4", "100.87.56.103", "192.168.1.1", "8.8.8.8"])
server1 = Server(["165.100.100.1"])
server.transfer(server1, 2)
class Test(unittest.TestCase):
    def load_test(self):
        self.assertEqual(server.get_load(), 3)
        self.assertEqual(server1.get_load(), 3)
    def user_test(self):
        for user in server.users:
            for user1 in server1.users:
                self.assertEqual(user is user1, False)
        for user in server.users:
            self.assertEqual(server.users.count(user), 1)
        for user in server1.users:
            self.assertEqual(server1.users.count(users), 1)

unittest.main()
