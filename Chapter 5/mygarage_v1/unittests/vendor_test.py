#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains test cases for testing the vendor_test.py code module.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v1
#
# Dr. Charles Bell, 2019
"""Unit test for the Vendor class
Usage: mysqlsh --py -f unittests/vendor_test.py"""
from __future__ import print_function

from unittests.crud_test import CRUDTest
from database.vendor import Vendor

class VendorTests(CRUDTest):
    """Test cases for the Vendor class"""

    def __init__(self):
        """Constructor"""
        CRUDTest.__init__(self)
        self.vendor = None
        self.last_id = None

    def set_up(self, mysql_x, user=None, passwd=None):
        """Setup the test cases"""
        self.mygarage = self.begin(mysql_x, "Vendor", user, passwd)
        self.vendor = Vendor(self.mygarage)

    def create(self):
        """Run Create test case"""
        print("\nCRUD: Create test case")
        vendor_data = {
            "Name": "ACME Bolt Company",
            "URL": "www.acme.org",
            "Sources": "looney toons"
        }
        self.vendor.create(vendor_data)
        self.last_id = self.mygarage.get_last_insert_id()[0]
        print("\tLast insert id = {0}".format(self.last_id))

    def read_all(self):
        """Run Read(all) test case"""
        print("\nCRUD: Read (all) test case")
        rows = self.vendor.read()
        self.show_rows(rows, 5)

    def read_one(self):
        """Run Read(record) test case"""
        print("\nCRUD: Read (row) test case")
        rows = self.vendor.read(self.last_id)
        print("\t{0}".format(", ".join(rows[0])))

    def update(self):
        """Run Update test case"""
        print("\nCRUD: Update test case")
        vendor_data = {
            "VendorId": self.last_id,
            "Name": "ACME Nut Company",
            "URL": "www.acme.org",
            "Sources": "looney toons"
        }
        self.vendor.update(vendor_data)

    def delete(self):
        """Run Delete test case"""
        print("\nCRUD: Delete test case")
        self.vendor.delete(self.last_id)
        rows = self.vendor.read(self.last_id)
        if not rows:
            print("\tNot found (deleted).")
