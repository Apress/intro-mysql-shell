#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a class that implements a NOSQL model for the
# MyGarage application. Included are the basic create, read, update,
# and delete methods for a table in the garage_v2 schema.
#
# Schema name = garage_v2
# Collection name = vendors
#
# Dr. Charles Bell, 2019
#
""" MyGarage Schema Collection Classes Version 2"""
from schema.garage_collection import GarageCollection

#
# Vendors collection
#
class Vendors(GarageCollection):
    """Vendors class

    This class encapsulates the vendors collection permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor - set collection name"""
        GarageCollection.__init__(self, mygarage, 'vendors')

    def check_create_prerequisites(self, doc_data):
        """Check prerequisites for the create operation."""
        vendor_name = doc_data.get("name", None)
        assert vendor_name, "You must supply a name for the vendor."
        return True
