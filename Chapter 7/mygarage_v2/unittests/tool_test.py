#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains test cases for testing the tool_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
"""Unit test for the Tools class
Usage: mysqlsh --py -f unittests/tool_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from schema.vendors import Vendors
from schema.tools import Tools

class ToolTests(CRUDTest):
    """Test cases for the Tools class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.tool = None
        self.last_id = None
        self.vendor_id = None
        self.vendors = None
        self.tools = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Tools", user, passwd)
        self.tools = Tools(self.mygarage)
        self.vendors = Vendors(self.mygarage)
        self.vendor_id = self.vendors.read()[0].get('_id', None)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        tool_data = {
            "vendorid": self.vendor_id,
            "size": "Left-handed Philips",
            "type": "Screwdriver",
            "category": "Handtool",
            "description": "#3 X 6-in"
        }
        self.tools.create(tool_data)
        self.last_id = self.tools.get_last_docid()
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        docs = self.tools.read()
        self.show_docs(docs, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (doc) test case")
        docs = self.tools.read(self.last_id)
        self.show_docs(docs, 1)

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        tool_data = {
            "_id": self.last_id,
            "size": "Right-handed Philips",
        }
        self.tools.update(tool_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.tools.delete(self.last_id)
        docs = self.tools.read(self.last_id)
        if not docs:
            print("\tNot found (deleted).")
