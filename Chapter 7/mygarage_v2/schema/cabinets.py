#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a class that implements a NOSQL model for the
# MyGarage application. Included are the basic create, read, update,
# and delete methods for a table in the garage_v2 schema.
#
# Schema name = garage_v2
# Collection name = cabinets
#
# Dr. Charles Bell, 2019
#
""" MyGarage Schema Collection Classes Version 2"""
from schema.garage_collection import GarageCollection
#
# Cabinets collection
#
class Cabinets(GarageCollection):
    """Cabinets class

    This class encapsulates the cabinets collection permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor - set collection name"""
        GarageCollection.__init__(self, mygarage, 'cabinets')

    def check_create_prerequisites(self, doc_data):
        """Check prerequisites for the create operation."""
        vendor_id = doc_data.get("vendorid", None)
        description = doc_data.get("description", None)
        location = doc_data.get("location", None)
        numdoors = doc_data.get("numdoors", None)
        assert vendor_id, "You must supply a vendor id for the cabinet."
        assert description, "You must supply a description for the cabinet."
        assert numdoors, "You must supply the number of doors for the cabinet."
        assert location, "You must supply a location for the cabinet."
        return True
#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a class that implements a NOSQL model for the
# MyGarage application. Included are the basic create, read, update,
# and delete methods for a table in the garage_v2 schema.
#
# Schema name = garage_v2
# Collection name = locations
#
# Dr. Charles Bell, 2019
#
""" MyGarage Schema Collection Classes Version 2"""
from schema.garage_collection import GarageCollection

#
# Workbench collection
#
class Locations(GarageCollection):
    """Locations class

    This class encapsulates the locations collection permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor - set collection name"""
        GarageCollection.__init__(self, mygarage, 'locations')

    def check_create_prerequisites(self, doc_data):
        """Check prerequisites for the create operation."""
        loc_type = doc_data.get("type", None)
        description = doc_data.get("description", None)
        assert loc_type, "You must supply a type for the location."
        assert description, "You must supply a description for the location."
        return True

    def remove_tool(self, tool_id):
        """Remove tool from this location."""
        location = self.col.find(':param1 in $.tool_ids').\
            bind('param1', tool_id).execute().fetch_all()
        if location:
            tool_locations = location[0]['tool_ids']
            tool_locations.remove(tool_id)
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
# Workbench collection
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
#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a class that implements a NOSQL model for the
# MyGarage application. Included are the basic create, read, update,
# and delete methods for a table in the garage_v2 schema.
#
# Schema name = garage_v2
# Collection name = shelving_units
#
# Dr. Charles Bell, 2019
#
""" MyGarage Schema Collection Classes Version 2"""
from schema.garage_collection import GarageCollection

#
# Workbench collection
#
class ShelvingUnits(GarageCollection):
    """ShelvingUnits class

    This class encapsulates the shelving_units collection permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor - set collection name"""
        GarageCollection.__init__(self, mygarage, 'shelving_units')

    def check_create_prerequisites(self, doc_data):
        """Check prerequisites for the create operation."""
        vendor_id = doc_data.get("vendorid", None)
        description = doc_data.get("description", None)
        location = doc_data.get("location", None)
        assert vendor_id, "You must supply a vendor id for the shelving_unit."
        assert description, "You must supply a description for the shelving_unit."
        assert location, "You must supply a location for the shelving_unit."
        return True
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
# Workbench collection
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
# Workbench collection
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
#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains a class that implements a NOSQL model for the
# MyGarage application. Included are the basic create, read, update,
# and delete methods for a table in the garage_v2 schema.
#
# Schema name = garage_v2
# Collection name = workbenches
#
# Dr. Charles Bell, 2019
#
""" MyGarage Schema Collection Classes Version 2"""
from schema.garage_collection import GarageCollection

#
# Workbench collection
#
class Workbenches(GarageCollection):
    """Workbenches class

    This class encapsulates the workbenchs collection permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor - set collection name"""
        GarageCollection.__init__(self, mygarage, 'workbenches')

    def check_create_prerequisites(self, doc_data):
        """Check prerequisites for the create operation."""
        vendor_id = doc_data.get("vendorid", None)
        description = doc_data.get("description", None)
        location = doc_data.get("location", None)
        assert vendor_id, "You must supply a vendor id for the workbench."
        assert description, "You must supply a description for the workbench."
        assert location, "You must supply a location for the workbench."
        return True
