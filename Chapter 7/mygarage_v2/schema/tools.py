#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a class that implements a NOSQL model for the
# MyGarage application. Included are the basic create, read, update,
# and delete methods for a table in the garage_v2 schema.
#
# Schema name = garage_v2
# Collection name = tools
#
# Dr. Charles Bell, 2019
#
""" MyGarage Schema Collection Classes Version 2"""
from schema.garage_collection import GarageCollection

TOOL_TYPES = [
    ('Adjustable Wrench', 'Adjustable Wrench'), ('Awl', 'Awl'),
    ('Clamp', 'Clamp'), ('Crowbar', 'Crowbar'), ('Drill Bit', 'Drill Bit'),
    ('File', 'File'), ('Hammer', 'Hammer'), ('Knife', 'Knife'), ('Level', 'Level'),
    ('Nutdriver', 'Nutdriver'), ('Pliers', 'Pliers'), ('Prybar', 'Prybar'),
    ('Router Bit', 'Router Bit'), ('Ruler', 'Ruler'), ('Saw', 'Saw'),
    ('Screwdriver', 'Screwdriver'), ('Socket', 'Socket'),
    ('Socket Wrench', 'Socket Wrench'), ('Wrench', 'Wrench'),
    ('Corded', 'Corded'), ('Cordless', 'Cordless'), ('Air', 'Air')
]

#
# Tools collection
#
class Tools(GarageCollection):
    """Cabinets class

    This class encapsulates the tools collection permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor - set collection name"""
        GarageCollection.__init__(self, mygarage, 'tools')

    def check_create_prerequisites(self, doc_data):
        """Check prerequisites for the create operation."""
        vendor_id = doc_data.get("vendorid", None)
        description = doc_data.get("description", None)
        tool_type = doc_data.get("type", None)
        category = doc_data.get("category", None)
        assert vendor_id, "You must supply a vendor id for the tool."
        assert description, "You must supply a description for the tool."
        assert category, "You must supply the category of tool (handtool or powertool) for the tool."
        assert tool_type, "You must supply category for the tool."
        return True
