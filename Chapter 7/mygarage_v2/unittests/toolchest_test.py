#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains test cases for testing the toolchest_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
"""Unit test for the Toolchests class
Usage: mysqlsh --py -f unittests/toolchest_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from schema.vendors import Vendors
from schema.toolchests import Toolchests

class ToolchestTests(CRUDTest):
    """Test cases for the Toolchests class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.toolchest = None
        self.last_id = None
        self.vendor_id = None
        self.vendors = None
        self.toolchests = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Toolchests", user, passwd)
        self.toolchests = Toolchests(self.mygarage)
        self.vendors = Vendors(self.mygarage)
        self.vendor_id = self.vendors.read()[0].get('_id', None)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        toolchest_data = {
            "vendorid": self.vendor_id,
            "description": "Kobalt 3000 Steel Rolling Tool Cabinet (Black)",
            "location": "Rear wall right of workbench",
            "drawers": [
                {
                    "depth": 17,
                    "description": "Top",
                    "height": 2,
                    "tool_ids": [
                        "00005cb1065c000000000000014c",
                        "00005cb1065c000000000000014d",
                        "00005cb1065c000000000000015c",
                        "00005cb1065c000000000000015d",
                        "00005cb1065c000000000000015f",
                        "00005cb1065c0000000000000160"
                    ],
                    "width": 21
                },
            ],
            "shelves": [
                {
                    "depth": 18,
                    "description": "Top",
                    "height": 5,
                    "width": 45
                },
            ],
            "depth": 22,
            "width": 48,
            "height": 54,
        }
        self.toolchests.create(toolchest_data)
        self.last_id = self.toolchests.get_last_docid()
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        docs = self.toolchests.read()
        self.show_docs(docs, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (doc) test case")
        docs = self.toolchests.read(self.last_id)
        self.show_docs(docs, 1)

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        toolchest_data = {
            "_id": self.last_id,
            "location": "Rear wall left of workbench",
            "drawers": [
                {
                    "depth": 17,
                    "description": "Top",
                    "height": 2,
                    "tool_ids": [
                        "00005cb1065c0000000000000160"
                    ],
                    "width": 21
                },
            ],
            "shelves": [
                {
                    "depth": 18,
                    "description": "Top",
                    "height": 5,
                    "width": 45
                },
                {
                    "depth": 18,
                    "description": "Bottom",
                    "height": 5,
                    "width": 45,
                    "tool_ids": [
                        "00005cb1065c000000000000014d",
                        "00005cb1065c000000000000015c",
                        "00005cb1065c000000000000015d",
                        "00005cb1065c000000000000015f",
                    ]
                },
            ],
            "depth": 22,
            "width": 48,
            "height": 54,
        }
        self.toolchests.update(toolchest_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.toolchests.delete(self.last_id)
        docs = self.toolchests.read(self.last_id)
        if not docs:
            print("\tNot found (deleted).")
