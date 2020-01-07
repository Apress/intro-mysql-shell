#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains to run all of the collection classes test cases.
#
# Note: This file is intended to be run from the shell.
#
# Database name = garage_v2
#
# Dr. Charles Bell, 2019
"""Run all unit tests for collection classes."""
from __future__ import print_function

from getpass import getpass
from unittests.cabinet_test import CabinetTests
from unittests.location_test import LocationTests
from unittests.organizer_test import OrganizerTests
from unittests.shelving_unit_test import ShelvingUnitTests
from unittests.toolchest_test import ToolchestTests
from unittests.tool_test import ToolTests
from unittests.vendor_test import VendorTests
from unittests.workbench_test import WorkbenchTests

print("CRUD Tests for all classes...")
crud_tests = []
cabinets = CabinetTests()
crud_tests.append(cabinets)
locations = LocationTests()
crud_tests.append(locations)
shelving_units = ShelvingUnitTests()
crud_tests.append(shelving_units)
toolchests = ToolchestTests()
crud_tests.append(toolchests)
tools = ToolTests()
crud_tests.append(tools)
organizers = OrganizerTests()
crud_tests.append(organizers)
vendors = VendorTests()
crud_tests.append(vendors)
workbenches = WorkbenchTests()
crud_tests.append(workbenches)

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
