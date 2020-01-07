#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains test cases for testing the vendors_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
"""Unit test for the Vendor class
Usage: mysqlsh --py -f unittests/vendor_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from schema.vendors import Vendors

class VendorTests(CRUDTest):
    """Test cases for the Vendors class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.vendors = None
        self.last_id = None
        self.vendors = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Vendors", user, passwd)
        self.vendors = Vendors(self.mygarage)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        vendor_data = {
            "name": "ACME Bolt Company",
            "url": "www.acme.org",
            "sources": "looney toons"
        }
        self.vendors.create(vendor_data)
        self.last_id = self.vendors.get_last_docid()
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        docs = self.vendors.read()
        self.show_docs(docs, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (doc) test case")
        docs = self.vendors.read(self.last_id)
        self.show_docs(docs, 1)

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        vendor_data = {
            "_id": self.last_id,
            "name": "ACME Nut Company",
            "url": "www.weesayso.co",
        }
        self.vendors.update(vendor_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.vendors.delete(self.last_id)
        docs = self.vendors.read(self.last_id)
        if not docs:
            print("\tNot found (deleted).")
