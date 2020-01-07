#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a class that implements a NOSQL model for the
# MyGarage application. Included are the basic create, read, update,
# and delete methods for a table in the garage_v2 schema.
#
# Schema name = garage_v2
# Collection name = organizers
#
# Dr. Charles Bell, 2019
#
""" MyGarage Schema Collection Classes Version 2"""
from schema.garage_collection import GarageCollection

ORGANIZER_TYPES = [
    ('Bag', 'Bag'), ('Basket', 'Basket'), ('Bin', 'Bin'),
    ('Box', 'Box'), ('Case', 'Case'), ('Crate', 'Crate')
]

#
# Organizers collection
#
class Organizers(GarageCollection):
    """Organizers class

    This class encapsulates the organizers collection permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor - set collection name"""
        GarageCollection.__init__(self, mygarage, 'organizers')

    def check_create_prerequisites(self, doc_data):
        """Check prerequisites for the create operation."""
        description = doc_data.get("description", None)
        org_type = doc_data.get("type", None)
        assert description, "You must supply a description for the organizer."
        assert org_type, "You must supply type for the organizer."
        return True

    def remove_tool(self, tool_id):
        """Remove a tool from the organizer."""
        location = self.col.find(':param1 in $.tool_ids').\
            bind('param1', tool_id).execute().fetch_all()
        if location:
            tool_locations = location[0]['tool_ids']
            tool_locations.remove(tool_id)
