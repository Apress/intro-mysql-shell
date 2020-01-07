#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains test cases for testing the cabinet_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
"""Unit test for the Cabinets class
Usage: mysqlsh --py -f unittests/cabinet_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from schema.vendors import Vendors
from schema.cabinets import Cabinets

class CabinetTests(CRUDTest):
    """Test cases for the Cabinets class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.cabinet = None
        self.last_id = None
        self.vendor_id = None
        self.vendors = None
        self.cabinets = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Cabinets", user, passwd)
        self.cabinets = Cabinets(self.mygarage)
        self.vendors = Vendors(self.mygarage)
        self.vendor_id = self.vendors.read()[0].get('_id', None)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        cabinet_data = {
            "vendorid": self.vendor_id,
            "description": "Large freestanding cabinet",
            "shelves": [
                {
                    "depth": 20,
                    "description": "Middle",
                    "height": 18,
                    "width": 48
                },
            ],
            "numdoors": 2,
            "width": 11,
            "depth": 11,
            "height": 11,
            "location": "Read wall next to compressor",
        }
        self.cabinets.create(cabinet_data)
        self.last_id = self.cabinets.get_last_docid()
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        docs = self.cabinets.read()
        self.show_docs(docs, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (doc) test case")
        docs = self.cabinets.read(self.last_id)
        self.show_docs(docs, 1)

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        cabinet_data = {
            "_id": self.last_id,
            "description": "Cold Storage",
            "shelves": [
                {
                    "depth": 20,
                    "description": "Top",
                    "height": 18,
                    "width": 48
                },
                {
                    "depth": 20,
                    "description": "Bottom",
                    "height": 18,
                    "width": 48,
                    "tool_ids": [
                        "00005cafa3eb00000000000007c5",
                        "00005cafa3eb00000000000007c6",
                        "00005cafa3eb00000000000007c7",
                    ],
                }
            ],
            "location": "3rd floor basement",
        }
        self.cabinets.update(cabinet_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.cabinets.delete(self.last_id)
        docs = self.cabinets.read(self.last_id)
        if not docs:
            print("\tNot found (deleted).")
