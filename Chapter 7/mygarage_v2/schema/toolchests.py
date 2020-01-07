#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a class that implements a NOSQL model for the
# MyGarage application. Included are the basic create, read, update,
# and delete methods for a table in the garage_v2 schema.
#
# Schema name = garage_v2
# Collection name = toolchests
#
# Dr. Charles Bell, 2019
#
""" MyGarage Schema Collection Classes Version 2"""
from schema.garage_collection import GarageCollection

#
# Toolchests collection
#
class Toolchests(GarageCollection):
    """Cabinets class

    This class encapsulates the toolchests collection permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor - set collection name"""
        GarageCollection.__init__(self, mygarage, 'toolchests')

    def check_create_prerequisites(self, doc_data):
        """Check prerequisites for the create operation."""
        vendor_id = doc_data.get("vendorid", None)
        description = doc_data.get("description", None)
        location = doc_data.get("location", None)
        assert vendor_id, "You must supply a vendor id for the toolchest."
        assert description, "You must supply a description for the toolchest."
        assert location, "You must supply a location for the toolchest."
        return True
