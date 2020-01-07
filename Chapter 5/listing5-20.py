from database.garage_v1 import MyGarage
VENDOR_COLS_CREATE = ['Name', 'URL', 'Sources']
class Vendor(object):
    def __init__(self, myg):
        self.mygarage = mygarage
        self.schema = mygarage.get_db()
        self.tbl = self.schema.get_table('vendor')
    
    def create(self, vendor_data):
        vendor_name = vendor_data.get("Name", None)
        link = vendor_data.get("URL", None)
        sources = vendor_data.get("Sources", None)
        self.tbl.insert(VENDOR_COLS_CREATE).values(vendor_name, link, sources).execute()
    

mygarage = MyGarage(mysqlx)
mygarage.connect('root', 'SECRET', 'localhost', 33060)
vendor = Vendor(mygarage)
vendor_data = {
    "Name": "ACME Bolt Company",
    "URL": "www.acme.org",
    "Sources": "looney toons"
}
    

vendor.create(vendor_data)
last_id = mygarage.get_last_insert_id()[0]
print("Last insert id = {0}".format(last_id))
