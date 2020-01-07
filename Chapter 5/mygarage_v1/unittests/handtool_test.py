#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains test cases for testing the handtool_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v1
#
# Dr. Charles Bell, 2019
"""Unit test for the Handtool class
Usage: mysqlsh --py -f unittests/handtool_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from database.handtool import Handtool

class HandtoolTests(CRUDTest):
    """Test cases for the Handtool class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.handtool = None
        self.last_id = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Handtool", user, passwd)
        self.handtool = Handtool(self.mygarage)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        handtool_data = {
            "VendorId": 101,
            "Description": "Plumpbus",
            "Type": 'Hammer',
            "ToolSize": 'medium',
            "PlaceId": 1001,
        }
        self.handtool.create(handtool_data)
        self.last_id = self.mygarage.get_last_insert_id()[0]
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        rows = self.handtool.read()
        self.show_rows(rows, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (row) test case")
        rows = self.handtool.read(self.last_id)
        print("\t{0}".format(", ".join(rows[0])))

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        handtool_data = {
            "HandtoolId": self.last_id,
            "VendorId": 101,
            "Description": "Plumpbus Pro",
            "Type": 'Screwdriver',
            "ToolSize": 'grande',
            "PlaceId": 1001,
        }
        self.handtool.update(handtool_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.handtool.delete(self.last_id)
        rows = self.handtool.read(self.last_id)
        if not rows:
            print("\tNot found (deleted).")
