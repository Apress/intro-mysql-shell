#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains a class that implements a relational database model
# for the MyGarage application. Included are the basic create, read,
# update, and delete methods for a table in the garage_v1 database.
#
# Database name = garage_v1
# Table name = storage
#
# Dr. Charles Bell, 2019
#
""" MyGarage Database Classes Version 1"""
from __future__ import print_function

#
# Constants
#
# Storage
STORAGE_TYPES = [
    ('Cabinet', 'Cabinet'), ('Shelving', 'Shelving'),
    ('Toolchest', 'Toolchest'), ('Workbench', 'Workbench')
]
STORAGE_COLS_BRIEF = [
    'storage.Id', 'Type', 'Description', 'Location'
]
STORAGE_COLS_CREATE = [
    'VendorId', 'Type', 'Description', 'NumDrawers', 'NumShelves', 'NumDoors',
    'Width', 'Depth', 'Height', 'Location'
]
STORAGE_COLS = []
STORAGE_COLS.extend(STORAGE_COLS_CREATE)
STORAGE_COLS.insert(0, 'Id') # Add the Id to the list
STORAGE_READ_LIST = (
    "SELECT storage.Id, vendor.name, Type, description, Location FROM "
    "garage_v1.storage JOIN garage_v1.vendor ON storage.VendorId = vendor.Id "
    "ORDER BY Type, Location"
)

#
# Storage table
#
class Storage(object):
    """Storage class

    This class encapsulates the storage table permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor"""
        self.mygarage = mygarage
        self.session = mygarage.get_session() # Needed for sql() calls
        self.schema = mygarage.get_db()
        self.tbl = self.schema.get_table('storage')

    def create(self, storage_data):
        """Add a new row to the table"""
        vendor_id = storage_data.get("VendorId", None)
        storage_type = storage_data.get("StorageType", None)
        description = storage_data.get("Description", None)
        num_drawers = storage_data.get("NumDrawers", 0)
        num_shelves = storage_data.get("NumShelves", 0)
        num_doors = storage_data.get("NumDoors", 0)
        width = storage_data.get("Width", 0)
        depth = storage_data.get("Depth", 0)
        height = storage_data.get("Height", 0)
        storage_location = storage_data.get("Location", None)
        assert vendor_id, "You must supply a vendorid for the storage."
        assert storage_type, "You must supply a type for the storage."
        assert description, "You must supply a description for the storage."
        assert storage_location, "You must supply a location for the storage."
        try:
            self.tbl.insert(STORAGE_COLS_CREATE).values(vendor_id, storage_type, description,
                                                        num_drawers, num_shelves, num_doors,
                                                        width, depth, height,
                                                        storage_location).execute()
        except Exception as err:
            print("ERROR: Cannot add storage: {0}".format(err))
            return (False, err)
        return (True, None)

    def read(self, storage_id=None, brief=False):
        """Read data from the table"""
        try:
            if brief:
                columns = STORAGE_COLS_BRIEF
            else:
                columns = STORAGE_COLS
            if not storage_id:
                # return all storage - uses a JOIN so we have to use the sql()
                # method instead of select, but we arrive at the same results
                sql_res = self.session.sql(STORAGE_READ_LIST).execute()
                return self.mygarage.make_rows_sql(sql_res, len(STORAGE_COLS_BRIEF))
            # return specific storage
            sql_res = self.tbl.select(columns).where(
                "Id = '{0}'".format(storage_id)).execute()
        except Exception as err:
            print("ERROR: Cannot read storage: {0}".format(err))
            return (False, err)
        return self.mygarage.make_rows(sql_res)

    def update(self, storage_data):
        """Update the data for a row in the table"""
        storage_id = storage_data.get("StorageId", None)
        vendor_id = storage_data.get("VendorId", None)
        storage_type = storage_data.get("StorageType", None)
        description = storage_data.get("Description", None)
        num_drawers = storage_data.get("NumDrawers", 0)
        num_shelves = storage_data.get("NumShelves", 0)
        num_doors = storage_data.get("NumDoors", 0)
        width = storage_data.get("Width", 0)
        depth = storage_data.get("Depth", 0)
        height = storage_data.get("Height", 0)
        storage_location = storage_data.get("Location", None)
        assert storage_id, "You must supply an Id to update the storage."
        assert vendor_id, "You must supply a vendorid for the storage."
        assert storage_type, "You must supply a type for the storage."
        assert description, "You must supply a description for the storage."
        assert storage_location, "You must supply a location for the storage."
        field_value_list = [
            ('VendorId', vendor_id),
            ('Type', storage_type),
            ('Description', description),
            ('NumDrawers', num_drawers),
            ('NumShelves', num_shelves),
            ('NumDoors', num_doors),
            ('Width', width),
            ('Depth', depth),
            ('Height', height),
            ('Location', storage_location)
        ]
        try:
            tbl_update = self.tbl.update()
            for field_value in field_value_list:
                tbl_update.set(field_value[0], field_value[1])
            tbl_update.where("Id = '{0}'".format(storage_id)).execute()
        except Exception as err:
            print("ERROR: Cannot update storage: {0}".format(err))
            return (False, err)
        return (True, None)

    def delete(self, storage_id=None):
        """Delete a row from the table"""
        assert storage_id, "You must supply an Id to delete the vendor."
        try:
            self.tbl.delete().where("Id = '{0}'".format(storage_id)).execute()
        except Exception as err:
            print("ERROR: Cannot delete storage: {0}".format(err))
            return (False, err)
        return (True, None)
