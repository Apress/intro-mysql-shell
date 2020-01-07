#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains test cases for testing the workbench_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
"""Unit test for the Workbenches class
Usage: mysqlsh --py -f unittests/workbench_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from schema.vendors import Vendors
from schema.workbenches import Workbenches

class WorkbenchTests(CRUDTest):
    """Test cases for the Wrokbenches class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.workbench = None
        self.last_id = None
        self.vendor_id = None
        self.vendors = None
        self.workbenches = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Workbenches", user, passwd)
        self.workbenches = Workbenches(self.mygarage)
        self.vendors = Vendors(self.mygarage)
        self.vendor_id = self.vendors.read()[0].get('_id', None)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        workbench_data = {
            "vendorid": self.vendor_id,
            "description": "Loft",
            "shelves": [
                {
                    "depth": 24,
                    "description": "Bottom Left",
                    "height": 10,
                    "width": 12
                },
                {
                    "depth": 24,
                    "description": "Bottom Right",
                    "height": 10,
                    "width": 12
                },
            ],
            "width": 11,
            "depth": 11,
            "height": 11,
            "location": "Ceiling",
        }
        self.workbenches.create(workbench_data)
        self.last_id = self.workbenches.get_last_docid()
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        docs = self.workbenches.read()
        self.show_docs(docs, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (doc) test case")
        docs = self.workbenches.read(self.last_id)
        self.show_docs(docs, 1)

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        workbench_data = {
            "_id": self.last_id,
            "description": "Cloud Storage",
            "drawers": [{
                "depth": 17,
                "description": "Top",
                "height": 4,
                "tool_ids": [
                    "00005cafa3eb00000000000007c5",
                    "00005cafa3eb00000000000007c6",
                    "00005cafa3eb00000000000007c7",
                ],
                "width": 21
            }],
            "location": "3rd floor basement",
        }
        self.workbenches.update(workbench_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.workbenches.delete(self.last_id)
        docs = self.workbenches.read(self.last_id)
        if not docs:
            print("\tNot found (deleted).")
