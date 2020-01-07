#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains a class that implements the base test class for the
# MyGarage sample application.
#
# Database name = garage_v1
#
# Dr. Charles Bell, 2019
#
"""Test setup and teardown methods to improve Unit tests"""
from __future__ import print_function

from getpass import getpass
from database.garage_v1 import MyGarage

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
    def show_rows(rows, num_rows):
        """Display N rows from row result"""
        print("\n\tFirst {0} rows:".format(num_rows))
        print("\t--------------------------")
        for item in range(0, num_rows):
            print("\t{0}".format(", ".join(rows[item])))

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
