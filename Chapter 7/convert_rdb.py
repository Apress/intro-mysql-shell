# Introducing MySQL 8 Shell
#
# Conversion script to convert RDBS to Document store for
# Chapter 7 sample application 'mygarage_v2'
#
# Dr. Charles Bell
import json

from getpass import getpass

try:
    input = raw_input
except NameError:
    pass

try:
    import mysqlx
except Exception:
    from mysqlsh import mysqlx

# Display the documents in a collection
def show_collection(col_object):
    print("\nCOLLECTION: {0}".format(col_object.name))
    results = col_object.find().execute().fetch_all()
    for document in results:
        print(json.dumps(json.loads(str(document)), indent=4, sort_keys=True))

# Get the storage places that match this storage id
def get_places(storage_id):
    return place_tbl.select('Type', 'Description', 'Width', 'Depth', 'Height', 'Id').where("StorageId = {0}".format(storage_id)).execute()

# Get the list of organizer ids at the storage place
def get_organizer_ids(place_id):
    organizer_ids = []
    org_results = organizer_tbl.select('Id').where("PlaceId = {0}".format(place_id)).execute()
    for org in org_results.fetch_all():
        organizer_ids.append(get_mapping(org[0], organizer_place_map)[0])
    return organizer_ids

# Get the list of handtool ids at the storage place
def get_handtool_ids(place_id):
    handtool_ids = []
    ht_results = handtool_tbl.select('Id').where("PlaceId = {0}".format(place_id)).execute()
    for ht in ht_results.fetch_all():
        handtool_ids.append(ht[0])
    return handtool_ids

# Get the list of powertool ids at the storage place
def get_powertool_ids(place_id):
    powertool_ids = []
    pt_results = powertool_tbl.select('Id').where("PlaceId = {0}".format(place_id)).execute()
    for pt in pt_results.fetch_all():
        powertool_ids.append(pt[0])
    return powertool_ids

# Get the new docid for the old vendor id
def get_mapping(old_id, mapping):
    for item in mapping:
        if item[0] == old_id:
            return item
    return None

# Search the organizers collection for the tool
def find_tool_in_organizers(tool_id):
    # organizers contain no shelves or drawers so fetch only the tool ids
    organizers = garage_v2.get_collection('organizers')
    results = organizers.find().fields("_id", "tool_ids", "type", "description").execute().fetch_all()
    for result in results:
        if (result["tool_ids"]) and (tool_id in result["tool_ids"]):
            return ("{0}, {1}".format(result["type"], result["description"]), 'organizers', result["_id"])
    return None

# Search for a tool in a given collection
def find_tool(collection_name, tool_id):
    collection = garage_v2.get_collection(collection_name)
    storage_places = collection.find().fields("_id", "description", "tool_locations").execute().fetch_all()
    for storage_place in storage_places:
        if storage_place["tool_locations"]:
            for location in storage_place["tool_locations"]:
                loc_data = locations.find('_id = :param1').bind('param1', location).execute().fetch_all()
                if loc_data:
                    loc_dict = dict(loc_data[0])
                    tool_ids = loc_dict.get("tool_ids", [])
                    if tool_id in tool_ids:
                        return ("{0}, {1} - {2}".format(storage_place["description"],
                                                  loc_dict["description"], loc_dict["type"]),
                                                  collection_name,
                                                  storage_place["_id"])
    return None

# Find the location document id for a tool.
def get_tool_location(tool_id):
    loc_found = find_tool_in_organizers(tool_id)
    if loc_found:
        return loc_found
    storage_collections = ['toolchests', 'shelving_units', 'workbenches', 'cabinets']
    for storage_collection in storage_collections:
        loc_found = find_tool(storage_collection, tool_id)
        if loc_found:
            return loc_found
    return None

# Get user id and password
userid = input("User Id: ")
passwd = getpass("Password: ")

user_info = {
    'host': 'localhost',
    'port': 33060,
    'user': userid,
    'password': passwd,
}

# Connect to the database garage_v1
my_session = mysqlx.get_session(user_info)
garage_v1 = my_session.get_schema('garage_v1')
# Get the tables
handtool_tbl = garage_v1.get_table('handtool')
organizer_tbl = garage_v1.get_table('organizer')
place_tbl = garage_v1.get_table('place')
powertool_tbl = garage_v1.get_table('powertool')
storage_tbl = garage_v1.get_table('storage')
vendor_tbl = garage_v1.get_table('vendor')

# Create the schema for garage_v2
my_session.drop_schema('garage_v2')
garage_v2 = my_session.create_schema('garage_v2')
# Create the collections
cabinets = garage_v2.create_collection('cabinets')
organizers = garage_v2.create_collection('organizers')
shelving_units = garage_v2.create_collection('shelving_units')
tools = garage_v2.create_collection('tools')
toolchests = garage_v2.create_collection('toolchests')
locations = garage_v2.create_collection('locations')
workbenches = garage_v2.create_collection('workbenches')
vendors = garage_v2.create_collection('vendors')

# Get the vendors
my_results = vendor_tbl.select('Id', 'Name', 'URL', 'Sources').execute()
vendor_id_map = []
for v_row in my_results.fetch_all():
    new_item = {
        'name': v_row[1],
        'url': v_row[2],
        'sources': v_row[3]
    }
    last_docid = vendors.add(new_item).execute().get_generated_ids()[0]
    vendor_id_map.append((v_row[0], last_docid))

show_collection(vendors)

# Get the tools combining the handtool and powertool tables
ht_results = handtool_tbl.select('Id', 'VendorId', 'Description', 'Type', 'Toolsize', 'PlaceId').execute()
tool_place_map = []
for ht_row in ht_results.fetch_all():
    new_item = {
        'category': 'Handtool',
        'vendorid': get_mapping(ht_row[1], vendor_id_map)[1],
        'description': ht_row[2],
        'type': ht_row[3],
        'size': ht_row[4],
    }
    last_docid = tools.add(new_item).execute().get_generated_ids()[0]
    tool_place_map.append((ht_row[0], last_docid))

pt_results = powertool_tbl.select('Id', 'VendorId', 'Description', 'Type', 'PlaceId').execute()
for pt_row in pt_results.fetch_all():
    new_item = {
        'category': 'Powertool',
        'vendorid': get_mapping(pt_row[1], vendor_id_map)[1],
        'description': pt_row[2],
        'type': pt_row[3],
    }
    last_docid = tools.add(new_item).execute().get_generated_ids()[0]
    tool_place_map.append((pt_row[0], last_docid))

show_collection(tools)

# Get organizers
org_results = organizer_tbl.select('Id', 'Description', 'Type', 'Width', 'Depth', 'Height', 'PlaceId').execute()
organizer_place_map = []
for org_row in org_results.fetch_all():
    tool_ids = get_handtool_ids(org_row[0])
    tool_ids.extend(get_powertool_ids(org_row[0]))
    tool_docids = [get_mapping(item, tool_place_map)[1] for item in tool_ids]
    new_item = {
        'description': org_row[1],
        'type': org_row[2],
        'width': org_row[3],
        'depth': org_row[4],
        'height': org_row[5],
    }
    if tool_docids:
        new_item.update({'tool_ids': tool_docids})
    last_docid = organizers.add(new_item).execute().get_generated_ids()[0]
    # We also need to save the mapping of organizers to storage places
    organizer_place_map.append((org_row[0], last_docid))

show_collection(organizers)

# Get the toolchests
tc_results = storage_tbl.select('Id', 'VendorId', 'Description', 'Width', 'Depth', 'Height', 'Location').where("Type = 'Toolchest'").execute()
# For each toolbox, get its storage places and insert into the collection
for tc_row in tc_results.fetch_all():
    new_tc = {
        'vendorid': get_mapping(tc_row[1], vendor_id_map)[1],
        'description': tc_row[2],
        'width': tc_row[3],
        'depth': tc_row[4],
        'height': tc_row[5],
        'location': tc_row[6],
    }
    _id = toolchests.add(new_tc).execute().get_generated_ids()[0]
    # Now, generate the tool locations for this document
    tool_locations = []
    for pl_row in get_places(tc_row[0]).fetch_all():
        # Get all organizers and tools that are placed here
        tool_ids = get_handtool_ids(pl_row[5])
        tool_ids.extend(get_powertool_ids(pl_row[5]))
        tool_docids = []
        org_ids = get_organizer_ids(pl_row[5])
        if org_ids:
            for org_id in org_ids:
                map_found = get_mapping(org_id, organizer_place_map)
                if map_found:
                    tool_docids.append(map_found[1])
        for item in tool_ids:
            map_found = get_mapping(item, tool_place_map)
            if map_found:
                tool_docids.append(map_found[1])
        if pl_row[0] == 'Shelf':
            new_item = {
                'type': 'Shelf',
                'description': pl_row[1],
                'width': pl_row[2],
                'depth': pl_row[3],
                'height': pl_row[4],
            }
            if tool_docids:
                new_item.update({'tool_ids': tool_docids})
            loc_id = locations.add(new_item).execute().get_generated_ids()[0]
            tool_locations.append(loc_id)
        else: # drawer is the only other value for type
            new_item = {
                'type': 'Drawer',
                'description': pl_row[1],
                'width': pl_row[2],
                'depth': pl_row[3],
                'height': pl_row[4],
            }
            if tool_docids:
                new_item.update({'tool_ids': tool_docids})
            loc_id = locations.add(new_item).execute().get_generated_ids()[0]
            tool_locations.append(loc_id)
    if len(tool_locations) > 0:
        toolchests.modify('_id = :param1') \
                  .bind('param1', _id) \
                  .set('tool_locations', tool_locations).execute()

show_collection(toolchests)

# Get the shelving units
su_results = storage_tbl.select('Id', 'VendorId', 'Description', 'Width', 'Depth', 'Height', 'Location').where("Type = 'Shelving'").execute()
# For each shelving unit, get its storage places and insert into the collection
for su_row in su_results.fetch_all():
    new_su = {
        'vendorid': get_mapping(su_row[1], vendor_id_map)[1],
        'description': su_row[2],
        'width': su_row[3],
        'depth': su_row[4],
        'height': su_row[5],
        'location': su_row[6],
    }
    _id = shelving_units.add(new_su).execute().get_generated_ids()[0]
    # Now, generate the tool locations for this document
    tool_locations = []
    for pl_row in get_places(su_row[0]).fetch_all():
        # Get all organizers and tools that are placed here
        tool_ids = get_handtool_ids(pl_row[5])
        tool_ids.extend(get_powertool_ids(pl_row[5]))
        tool_ids.extend(get_organizer_ids(pl_row[5]))
        tool_docids = []
        for item in tool_ids:
            map_found = get_mapping(item, tool_place_map)
            if map_found:
                tool_docids.append(map_found[1])
                continue
            map_found = get_mapping(item, organizer_place_map)
            if map_found:
                tool_docids.append(map_found[1])

        if pl_row[0] == 'Shelf':
            new_item = {
                'type': 'Shelf',
                'description': pl_row[1],
                'width': pl_row[2],
                'depth': pl_row[3],
                'height': pl_row[4],
            }
            if tool_docids:
                new_item.update({'tool_ids': tool_docids})
            loc_id = locations.add(new_item).execute().get_generated_ids()[0]
            tool_locations.append(loc_id)
    if len(tool_locations) > 0:
        shelving_units.modify('_id = :param1') \
                        .bind('param1', _id) \
                        .set('tool_locations', tool_locations).execute()

show_collection(shelving_units)

# Get the cabinets
cab_results = storage_tbl.select('Id', 'VendorId', 'Description', 'Width', 'Depth', 'Height', 'Location', 'NumDoors').where("Type = 'Cabinet'").execute()
# For each shelving unit, get its storage places and insert into the collection
for cab_row in cab_results.fetch_all():
    new_cab = {
        'vendorid': get_mapping(cab_row[1], vendor_id_map)[1],
        'description': cab_row[2],
        'width': cab_row[3],
        'depth': cab_row[4],
        'height': cab_row[5],
        'location': cab_row[6],
        'numdoors': cab_row[7],
    }
    _id = cabinets.add(new_cab).execute().get_generated_ids()[0]
    # Now, generate the tool locations for this document
    tool_locations = []
    for pl_row in get_places(cab_row[0]).fetch_all():
        # Get all organizers and tools that are placed here
        tool_ids = get_handtool_ids(pl_row[5])
        tool_ids.extend(get_powertool_ids(pl_row[5]))
        tool_ids.extend(get_organizer_ids(pl_row[5]))
        tool_docids = []
        for item in tool_ids:
            map_found = get_mapping(item, tool_place_map)
            if map_found:
                tool_docids.append(map_found[1])
                continue
            map_found = get_mapping(item, organizer_place_map)
            if map_found:
                tool_docids.append(map_found[1])
        if pl_row[0] == 'Shelf':
            new_item = {
                'type': 'Shelf',
                'description': pl_row[1],
                'width': pl_row[2],
                'depth': pl_row[3],
                'height': pl_row[4],
            }
            if tool_docids:
                new_item.update({'tool_ids': tool_docids})
            loc_id = locations.add(new_item).execute().get_generated_ids()[0]
            tool_locations.append(loc_id)
    if len(tool_locations) > 0:
        cabinets.modify('_id = :param1') \
                .bind('param1', _id) \
                .set('tool_locations', tool_locations).execute()

show_collection(cabinets)

# Get the workbenches
wb_results = storage_tbl.select('Id', 'VendorId', 'Description', 'Width', 'Depth', 'Height', 'Location').where("Type = 'Workbench'").execute()
# For each workbench, get its storage places and insert into the collection
for wb_row in wb_results.fetch_all():
    new_wb = {
        'vendorid': get_mapping(wb_row[1], vendor_id_map)[1],
        'description': wb_row[2],
        'width': wb_row[3],
        'depth': wb_row[4],
        'height': wb_row[5],
        'location': wb_row[6],
    }
    _id = workbenches.add(new_wb).execute().get_generated_ids()[0]
    # Now, generate the tool locations for this document
    tool_locations = []
    for pl_row in get_places(wb_row[0]).fetch_all():
        # Get all organizers and tools that are placed here
        tool_ids = get_handtool_ids(pl_row[5])
        tool_ids.extend(get_powertool_ids(pl_row[5]))
        tool_ids.extend(get_organizer_ids(pl_row[5]))
        tool_docids = []
        for item in tool_ids:
            map_found = get_mapping(item, tool_place_map)
            if map_found:
                tool_docids.append(map_found[1])
                continue
            map_found = get_mapping(item, organizer_place_map)
            if map_found:
                tool_docids.append(map_found[1])
        if pl_row[0] == 'Shelf':
            new_item = {
                'type': 'Shelf',
                'description': pl_row[1],
                'width': pl_row[2],
                'depth': pl_row[3],
                'height': pl_row[4],
            }
            if tool_docids:
                new_item.update({'tool_ids': tool_docids})
            loc_id = locations.add(new_item).execute().get_generated_ids()[0]
            tool_locations.append(loc_id)
    if len(tool_locations) > 0:
        workbenches.modify('_id = :param1') \
                   .bind('param1', _id) \
                   .set('tool_locations', tool_locations).execute()

show_collection(workbenches)

# Add the location for each tool
tool_results = tools.find().execute().fetch_all()
for tool in tool_results:
    _id = tool["_id"]
    try:
        location = get_tool_location(_id)
        if location:
            r = tools.modify('_id = :param1').bind('param1', _id).set('location', location[0]).execute()
    except Exception as err:
        print(err)
        exit(1)

show_collection(tools)

# Add the location for each organizer
org_results = organizers.find().execute().fetch_all()
for org in org_results:
    _id = org["_id"]
    try:
        location = get_tool_location(_id)
        if location:
            r = organizers.modify('_id = :param1').bind('param1', _id).set('location', location[0]).execute()
    except Exception as err:
        print(err)

show_collection(organizers)
show_collection(locations)
