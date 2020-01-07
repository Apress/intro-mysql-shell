#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a class that implements the base test class for the
# MyGarage sample application.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
#
"""Test setup and teardown methods to improve Unit tests"""
from __future__ import print_function

import json

from getpass import getpass
from schema.garage_v2 import MyGarage

class CRUDTest(object):
    """Base class for Unit testing table/view classes."""

    def __init__(self):
        """Constructor"""
        self.mygarage = None

    def begin(self, mysql_x, class_name, user=None, passwd=None):
        """Start the tests"""
        print("\n*** {0} Class Unit test ***\n".format(class_name))
        self.mygarage = MyGarage(mysql_x)
        if not user:
            user = raw_input("User: ")
        if not passwd:
            passwd = getpass("Password: ")
        print("Connecting...")
        self.mygarage.connect(user, passwd, 'localhost', 33060)
        return self.mygarage

    @staticmethod
    def show_docs(docs, num_docs):
        """Display N docs from row result"""
        if len(docs) < int(num_docs):
            num_docs = len(docs)
        print("\nFirst {0} docs:".format(num_docs))
        print("--------------------------")
        for item in range(0, num_docs):
            print(json.dumps(json.loads(str(docs[item])), indent=4, sort_keys=True), end='')
            if item < (num_docs-1):
                print(",")
        print("")

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup functions"""
        pass

    def create(self):
        """Run Create test case"""
        pass

    def read_all(self):
        """Run Read(all) test case"""
        pass

    def read_one(self):
        """Run Read(record) test case"""
        pass

    def udpate(self):
        """Run Update test case"""
        pass

    def delete(self):
        """Run Delete test case"""
        pass

    def tear_down(self):
        """Tear down functions"""
        print("\nDisconnecting...")
        self.mygarage.disconnect()
