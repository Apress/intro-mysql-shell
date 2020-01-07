#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains to run all of the database classes test cases.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v1
#
# Dr. Charles Bell, 2019
"""Run all unit tests for table/view classes."""
from __future__ import print_function

from getpass import getpass
from unittests.handtool_test import HandtoolTests
from unittests.location_test import LocationTests
from unittests.organizer_test import OrganizerTests
from unittests.place_test import PlaceTests
from unittests.powertool_test import PowertoolTests
from unittests.storage_test import StorageTests
from unittests.vendor_test import VendorTests

print("CRUD Tests for all classes...")
crud_tests = []
handtool = HandtoolTests()
crud_tests.append(handtool)
location = LocationTests()
crud_tests.append(location)
organizer = OrganizerTests()
crud_tests.append(organizer)
place = PlaceTests()
crud_tests.append(place)
powertool = PowertoolTests()
crud_tests.append(powertool)
storage = StorageTests()
crud_tests.append(storage)
vendor = VendorTests()
crud_tests.append(vendor)

# Get user, passwd
user = raw_input("User: ")
passwd = getpass("Password: ")

# Run the CRUD operations for all classes that support them
# pylint: disable=undefined-variable
for test in crud_tests:
    test.set_up(mysqlx, user, passwd)
    test.create()
    test.read_one()
    test.read_all()
    test.update()
    test.read_one()
    test.delete()
    test.tear_down()

# pylint: enable=undefined-variable
