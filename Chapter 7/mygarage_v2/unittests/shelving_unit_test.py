#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains test cases for testing the shelving_unit_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
"""Unit test for the ShelvingUnits class
Usage: mysqlsh --py -f unittests/shelving_unit_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from schema.vendors import Vendors
from schema.shelving_units import ShelvingUnits

class ShelvingUnitTests(CRUDTest):
    """Test cases for the ShelvingUnits class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.shelving_unit = None
        self.last_id = None
        self.vendor_id = None
        self.vendors = None
        self.shelving_units = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "ShelvingUnits", user, passwd)
        self.shelving_units = ShelvingUnits(self.mygarage)
        self.vendors = Vendors(self.mygarage)
        self.vendor_id = self.vendors.read()[0].get('_id', None)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        shelving_unit_data = {
            "vendorid": self.vendor_id,
            "description": "Wire shelving #3",
            "location": "Right wall",
            "shelves": [
                {
                    "depth": 24,
                    "description": "Top",
                    "height": 18,
                    "width": 48
                },
                {
                    "depth": 24,
                    "description": "Bottom",
                    "height": 18,
                    "width": 48
                }
            ],
            "depth": 24,
            "width": 48,
            "height": 72,
        }
        self.shelving_units.create(shelving_unit_data)
        self.last_id = self.shelving_units.get_last_docid()
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        docs = self.shelving_units.read()
        self.show_docs(docs, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (doc) test case")
        docs = self.shelving_units.read(self.last_id)
        self.show_docs(docs, 1)

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        shelving_unit_data = {
            "_id": self.last_id,
            "shelves": [
                {
                    "depth": 24,
                    "description": "Top",
                    "height": 18,
                    "width": 48
                },
                {
                    "depth": 24,
                    "description": "Middle",
                    "height": 18,
                    "width": 48,
                    "tool_ids": [
                        "00005cafa3eb00000000000007c5",
                        "00005cafa3eb00000000000007c6",
                        "00005cafa3eb00000000000007c7",
                    ],
                },
                {
                    "depth": 24,
                    "description": "Bottom",
                    "height": 18,
                    "width": 48
                }
            ],
        }
        self.shelving_units.update(shelving_unit_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.shelving_units.delete(self.last_id)
        docs = self.shelving_units.read(self.last_id)
        if not docs:
            print("\tNot found (deleted).")
