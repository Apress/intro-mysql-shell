#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains test cases for testing the location_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
"""Unit test for the Locations class
Usage: mysqlsh --py -f unittests/location_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from schema.vendors import Vendors
from schema.locations import Locations

class LocationTests(CRUDTest):
    """Test cases for the Locations class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.tool = None
        self.last_id = None
        self.vendor_id = None
        self.vendors = None
        self.locations = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Locations", user, passwd)
        self.locations = Locations(self.mygarage)
        self.vendors = Vendors(self.mygarage)
        self.vendor_id = self.vendors.read()[0].get('_id', None)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        location_data = {
            "type": "Shelf",
            "description": "Top",
            "height": 4,
            "width": 5,
            "depth": 12,
            "tool_ids": [
                "00005cb8f74200000000000003bd",
                "00005cb8f74200000000000003bf",
                "00005cb8f74200000000000003c2",
                "00005cb8f74200000000000003c3",
                "00005cb8f74200000000000003c4",
                "00005cb8f74200000000000003c7",
                "00005cb8f74200000000000003c8",
            ]
        }
        self.locations.create(location_data)
        self.last_id = self.locations.get_last_docid()
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        docs = self.locations.read()
        self.show_docs(docs, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (doc) test case")
        docs = self.locations.read(self.last_id)
        self.show_docs(docs, 1)

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        location_data = {
            "_id": self.last_id,
            "type": "Drawer",
            "description": "Bottom",
            "height": 2,
            "width": 22,
            "depth": 18,
            "tool_ids": [
                "00005cb8f74200000000000003c7",
                "00005cb8f74200000000000003c8",
            ]
        }
        self.locations.update(location_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.locations.delete(self.last_id)
        docs = self.locations.read(self.last_id)
        if not docs:
            print("\tNot found (deleted).")
