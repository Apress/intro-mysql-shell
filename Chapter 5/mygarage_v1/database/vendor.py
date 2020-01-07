#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains a class that implements a relational database model
# for the MyGarage application. Included are the basic create, read,
# update, and delete methods for a table in the garage_v1 database.
#
# Database name = garage_v1
# Table name = vendor
#
# Dr. Charles Bell, 2019
#
""" MyGarage Database Classes Version 1"""
from __future__ import print_function

#
# Constants
#
# Vendor
VENDOR_COLS_CREATE = ['Name', 'URL', 'Sources']
VENDOR_COLS = []
VENDOR_COLS.extend(VENDOR_COLS_CREATE)
VENDOR_COLS.insert(0, 'Id') # Add the Id to the list

#
# Vendor table
#
class Vendor(object):
    """Vendor class

    This class encapsulates the vendor table permitting CRUD operations
    on the data.
    """
    def __init__(self, mygarage):
        """Constructor"""
        self.mygarage = mygarage
        self.schema = mygarage.get_db()
        self.tbl = self.schema.get_table('vendor')

    def create(self, vendor_data):
        """Add a new row to the table"""
        vendor_name = vendor_data.get("Name", None)
        link = vendor_data.get("URL", None)
        sources = vendor_data.get("Sources", None)
        assert vendor_name, "You must supply a name for the vendor."
        try:
            self.tbl.insert(VENDOR_COLS_CREATE).values(vendor_name, link, sources).execute()
        except Exception as err:
            print("ERROR: Cannot add vendor: {0}".format(err))
            return (False, err)
        return (True, None)

    def read(self, vendor_id=None):
        """Read data from the table"""
        if not vendor_id:
            # return all vendors
            sql_res = self.tbl.select(VENDOR_COLS).order_by("Name").execute()
        else:
            # return specific vendor
            sql_res = self.tbl.select(VENDOR_COLS).where(
                "Id = '{0}'".format(vendor_id)).execute()
        return self.mygarage.make_rows(sql_res)

    def update(self, vendor_data):
        """Update the data for a row in the table"""
        vendor_id = vendor_data.get("VendorId", None)
        vendor_name = vendor_data.get("Name", None)
        link = vendor_data.get("URL", None)
        sources = vendor_data.get("Sources", None)
        assert vendor_id, "You must supply an Id to update the vendor."
        field_value_list = [('Name', vendor_name), ('URL', link), ('Sources', sources)]
        try:
            tbl_update = self.tbl.update()
            for field_value in field_value_list:
                tbl_update.set(field_value[0], field_value[1])
            tbl_update.where("Id = '{0}'".format(vendor_id)).execute()
        except Exception as err:
            print("ERROR: Cannot update vendor: {0}".format(err))
            return (False, err)
        return (True, None)

    def delete(self, vendor_id=None):
        """Delete a row from the table"""
        assert vendor_id, "You must supply an Id to delete the vendor."
        try:
            self.tbl.delete().where("Id = '{0}'".format(vendor_id)).execute()
        except Exception as err:
            print("ERROR: Cannot delete vendor: {0}".format(err))
            return (False, err)
        return (True, None)
