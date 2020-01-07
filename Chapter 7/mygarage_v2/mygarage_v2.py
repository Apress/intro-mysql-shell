#
# Introducing the MySQL Shell - MyGarage Version 2
#
# This file contains the sample Python + Flask application for demonstrating
# how to build a NOSQL application. Thus, it relies on a set of classes that
# encapsulates the CRUD operations for a MySQL document store.
#
# Dr. Charles Bell, 2019
#
# python -m pylint --rcfile=pylint.rc
#
""" MyGarage Flask Application Version 2"""
from __future__ import print_function

from getpass import getpass
from flask import Flask, render_template, request, redirect, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (HiddenField, TextField, SelectField, IntegerField, SubmitField)
from wtforms.validators import Required, Length

from schema.garage_v2 import MyGarage, make_list
from schema.cabinets import Cabinets
from schema.locations import Locations
from schema.organizers import Organizers, ORGANIZER_TYPES
from schema.shelving_units import ShelvingUnits
from schema.toolchests import Toolchests
from schema.tools import Tools, TOOL_TYPES
from schema.vendors import Vendors
from schema.workbenches import Workbenches

# pylint: disable=redefined-builtin
try:
    input = raw_input
except NameError:
    pass
# pylint: enable=redefined-builtin

#
# Strings
#
REQUIRED = "{0} field is required."
RANGE = "{0} range is {1} to {2} characters."
TOOL_LOCATIONS_COLUMNS = (
    '<td style="width:100px"><b>Type</b></td>',
    '<td style="width:300px"><b>Description</b></td>',
    '<td style="width:100px"><b>Category</b></td>',
    '<td style="width:100px"><b>Size</b></td>',
)
TOOL_COLUMNS_ORGANIZER = (
    '<td style="width:100px"><b>Type</b></td>',
    '<td style="width:200px"><b>Description</b></td>',
    '<td style="width:100px"><b>Category</b></td>',
    '<td style="width:100px"><b>Size</b></td>',
)
TOOL_COLUMNS = (
    '<td style="width:100px"><b>Category</b></td>',
    '<td style="width:100px"><b>Type</b></td>',
    '<td style="width:100px"><b>Size</b></td>',
    '<td style="width:200px"><b>Description</b></td>',
    '<td style="width:400px"><b>Location</b></td>',
)

#
# Setup Flask, Bootstrap, and security.
#
app = Flask(__name__)
app.config['SECRET_KEY'] = "He says, he's already got one!"
manager = Manager(app)
bootstrap = Bootstrap(app)

#
# Utility functions
#
def flash_errors(form):
    """Display errors in the flash message bar."""
    for error in form.errors:
        flash("{0} : {1}".format(error, ",".join(form.errors[error])))

#
# Customized fields for skipping prevalidation
#
class NewSelectField(SelectField):
    """Create a select field for selecting complex entries."""
    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        # pylint: disable=attribute-defined-outside-init
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""
        # pylint: enable=attribute-defined-outside-init

#
# Form classes - the forms for the application
#
class ListForm(FlaskForm):
    """List form class for displaying a list of rows."""
    form_name = TextField('Form_Name')
    submit = SubmitField('New')
    back_button = SubmitField('Back')

class LocationForm(FlaskForm):
    """Storage Place form class"""
    storageid = HiddenField('Id')
    storage_place = HiddenField('StoragePlace')
    placetype = NewSelectField("Type")
    description = TextField(
        'Description',
        validators=[Required(message=REQUIRED.format("Description")),
                    Length(min=1, max=125, message=RANGE.format("Description", 1, 125))]
    )
    width = IntegerField('Width')
    depth = IntegerField('Depth')
    height = IntegerField('Height')
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    close_button = SubmitField('Close')

class OrganizerForm(FlaskForm):
    """Organizer form class"""
    organizerid = HiddenField('Id')
    description = TextField(
        'Description',
        validators=[Required(message=REQUIRED.format("Description")),
                    Length(min=1, max=125, message=RANGE.format("Description", 1, 125))]
    )
    width = IntegerField('Width')
    depth = IntegerField('Depth')
    height = IntegerField('Height')
    location = NewSelectField('Location')
    organizertype = NewSelectField(
        'Type',
        validators=[Required(message=REQUIRED.format("Type"))],
        choices=ORGANIZER_TYPES,
    )
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    close_button = SubmitField('Close')

class StoragePlaceForm(FlaskForm):
    """Storage Place form class"""
    vendorid = HiddenField('VendorId')
    storageid = HiddenField('Id')
    vendor = NewSelectField(
        'Vendor', validators=[Required(message=REQUIRED.format("Vendor"))]
    )
    description = TextField(
        'Description',
        validators=[Required(message=REQUIRED.format("Description")),
                    Length(min=1, max=125, message=RANGE.format("Description", 1, 125))]
    )
    numdoors = IntegerField('Num Doors')
    width = IntegerField('Width')
    depth = IntegerField('Depth')
    height = IntegerField('Height')
    location = TextField('Physical Location')
    caption = TextField('Caption')
    manage_tool_locations_button = SubmitField('Manage Tool Locations')
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    close_button = SubmitField('Close')

class ToolForm(FlaskForm):
    """Tool form class"""
    vendorid = HiddenField('VendorId')
    toolid = HiddenField('Id')
    vendor = NewSelectField(
        'Vendor', validators=[Required(message=REQUIRED.format("Vendor"))]
    )
    description = TextField(
        'Description',
        validators=[Required(message=REQUIRED.format("Description")),
                    Length(min=1, max=125, message=RANGE.format("Description", 1, 125))]
    )
    category = NewSelectField(
        'Category',
        validators=[Required(message=REQUIRED.format("Category"))],
        choices=[('Handtool', 'Handtool'), ('Powertool', 'Powertool')]
    )
    tooltype = NewSelectField(
        'Type',
        validators=[Required(message=REQUIRED.format("Type"))],
        choices=TOOL_TYPES
    )
    toolsize = TextField('ToolSize')
    location = NewSelectField('Location')
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    close_button = SubmitField('Close')

class VendorForm(FlaskForm):
    """Vendor form class"""
    vendorid = HiddenField('_id')
    name = TextField(
        'Name',
        validators=[Required(message=REQUIRED.format("Name")),
                    Length(min=1, max=50, message=RANGE.format("Name", 1, 50))]
        )
    url = TextField(
        'URL', validators=[Required(message=REQUIRED.format("URL")),
                           Length(min=0, max=125, message=RANGE.format("URL", 0, 125))]
    )
    sources = TextField(
        'Sources',
        validators=[Required(message=REQUIRED.format("Sources")),
                    Length(min=0, max=40, message=RANGE.format("Sources", 0, 40))]
    )
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    close_button = SubmitField('Close')

#
# Routing functions - the following defines the routing functions for the
# menu items.
#

#
# Simple List
#
# This is the default page for "home" and listing objects. It reuses a single
# template "list.html" to show a list of rows from the schema. Built into
# each row is a special edit link for editing any of the rows, which redirects
# to the appropriate route (form).
#
# pylint: disable=too-many-return-statements, too-many-statements
@app.route('/', methods=['GET', 'POST'])
@app.route('/list/<string:kind>', methods=['GET', 'POST'])
@app.route('/list/<string:kind>/<string:storage_type>/<string:docid>', methods=['GET', 'POST'])
def simple_list(kind=None, storage_type=None, docid=None):
    """Display the simple list and landing page"""
    form = ListForm()
    if kind == 'cabinets':
        form.form_name.label = 'Cabinets'
        if request.method == 'POST':
            return redirect('storage_places/cabinets')
        columns = (
            '<td style="width:500px"><b>Description</b></td>',
            '<td style="width:300px"><b>Location</b></td>',
        )
        kind = 'cabinets'
        cabinet_data = Cabinets(mygarage)
        rows = make_list(cabinet_data.read(),
                         ['_id', 'description', 'location'])
        del form.back_button
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind, redirect='storage_places')
    elif kind == 'organizers':
        form.form_name.label = 'Organizers'
        if request.method == 'POST':
            return redirect('organizers')
        columns = (
            '<td style="width:100px"><b>Type</b></td>',
            '<td style="width:300px"><b>Description</b></td>',
            '<td style="width:400px"><b>Location</b></td>',
        )
        kind = 'organizers'
        organizer_data = Organizers(mygarage)
        rows = make_list(organizer_data.read(),
                         ['_id', 'type', 'description', 'location'])
        del form.back_button
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind, redirect='storage_places')
    elif kind == 'shelving_units':
        form.form_name.label = 'Shelving_units'
        if request.method == 'POST':
            return redirect('storage_places/shelving_units')
        columns = (
            '<td style="width:300px"><b>Description</b></td>',
            '<td style="width:400px"><b>Location</b></td>',
        )
        kind = 'shelving_units'
        workbench_data = ShelvingUnits(mygarage)
        rows = make_list(workbench_data.read(),
                         ['_id', 'description', 'location'])
        del form.back_button
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind, redirect='storage_places')
    elif kind == 'toolchests' or not kind:
        form.form_name.label = 'Toolchests'
        if request.method == 'POST':
            return redirect('storage_places/toolchests')
        columns = (
            '<td style="width:300px"><b>Description</b></td>',
            '<td style="width:400px"><b>Location</b></td>',
        )
        kind = 'toolchests'
        toolchest_data = Toolchests(mygarage)
        rows = make_list(toolchest_data.read(),
                         ['_id', 'description', 'location'])
        del form.back_button
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind, redirect='storage_places')
    elif kind == 'tools':
        form.form_name.label = 'Tools'
        if request.method == 'POST':
            return redirect('tools')
        columns = TOOL_COLUMNS
        kind = 'tools'
        workbench_data = Tools(mygarage)
        rows = make_list(workbench_data.read(),
                         ['_id', 'category', 'type', 'size', 'description', 'location'])
        del form.back_button
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind, redirect=None)
    elif kind == 'vendors':
        form.form_name.label = 'Vendors'
        if request.method == 'POST':
            return redirect('vendors')
        columns = (
            '<td style="width:200px"><b>Name</b></td>',
            '<td style="width:400px"><b>URL</b></td>',
            '<td style="width:200px"><b>Sources</b></td>',
        )
        kind = 'vendors'
        vendor_data = Vendors(mygarage)
        rows = make_list(vendor_data.read(),
                         ['_id', 'name', 'url', 'sources'])
        del form.back_button
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind, redirect=None)
    elif kind == 'workbenches':
        form.form_name.label = 'Workbenches'
        if request.method == 'POST':
            return redirect('storage_places/workbenches')
        columns = (
            '<td style="width:300px"><b>Description</b></td>',
            '<td style="width:400px"><b>Location</b></td>',
        )
        kind = 'workbenches'
        workbench_data = Workbenches(mygarage)
        rows = make_list(workbench_data.read(),
                         ['_id', 'description', 'location'])
        del form.back_button
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind, redirect='storage_places')
    elif kind == 'tool_locations':
        label_str = storage_type.rstrip('s').replace('_', ' ')
        form.form_name.label = 'Tool locations for {0}'.format(label_str)
        if request.method == 'POST':
            if form.submit.data:
                return redirect('/tool_locations/{0}/{1}'.format(storage_type, docid))
            return redirect('/storage_places/{0}/{1}'.format(storage_type, docid))
        columns = (
            '<td style="width:100px"><b>Type</b></td>',
            '<td style="width:300px"><b>Description</b></td>',
            '<td style="width:100px"><b>Height</b></td>',
            '<td style="width:100px"><b>Width</b></td>',
            '<td style="width:100px"><b>Depth</b></td>',
        )
        if storage_type == 'cabinets':
            collection = Cabinets(mygarage)
        elif storage_type == 'shelving_units':
            collection = ShelvingUnits(mygarage)
        elif storage_type == 'toolchests':
            collection = Toolchests(mygarage)
        else:
            collection = Workbenches(mygarage)
        locations = collection.get_tool_locations(docid)
        rows = []
        for item in locations:
            loc_dict = dict(item)
            rows.append((loc_dict.get("_id"), loc_dict.get("type", None),
                         loc_dict.get("description", None),
                         loc_dict.get("height", None),
                         loc_dict.get("width", None), loc_dict.get("depth", None)))
        return render_template("list.html", form=form, rows=rows,
                               columns=columns,
                               kind='tool_location/{0}/{1}'.format(storage_type, docid),
                               redirect=None)
    else:
        flash("Something is wrong. No 'kind' specified for list. "
              "Got this: {0}".format(kind))
    return None
# pylint: enable=too-many-return-statements, too-many-statements

#
# Location
#
# This page allows creating and editing tool location documents.
#
# pylint: disable=too-many-statements, too-many-locals
@app.route('/tool_locations', methods=['GET', 'POST'])
@app.route('/tool_location/<string:storage_type>/<string:docid>/<string:locid>',
           methods=['GET', 'POST'])
@app.route('/tool_locations/<string:storage_type>/<string:docid>', methods=['GET', 'POST'])
def location(locid=None, docid=None, storage_type=None):
    """Manage tool_location CRUD operations."""
    # Get data from the form if present
    form = LocationForm()
    locations = Locations(mygarage)
    if storage_type == 'cabinets':
        collection = Cabinets(mygarage)
        place_types = [('Shelf', 'Shelf')]
        storage_place_name = 'Cabinet'
    elif storage_type == 'shelving_units':
        collection = ShelvingUnits(mygarage)
        place_types = [('Drawer', 'Drawer'), ('Shelf', 'Shelf')]
        storage_place_name = 'Shelving Unit'
    elif storage_type == 'toolchests':
        collection = Toolchests(mygarage)
        place_types = [('Drawer', 'Drawer'), ('Shelf', 'Shelf')]
        storage_place_name = 'Toolchest'
    else:
        collection = Workbenches(mygarage)
        place_types = [('Drawer', 'Drawer'), ('Shelf', 'Shelf')]
        storage_place_name = 'Workbench'
    # Get data from the form if present
    form_desc = form.description.data
    form_height = form.height.data
    form_width = form.width.data
    form_depth = form.depth.data
    form_type = form.placetype.data
    form.placetype.choices = place_types
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if locid:
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = locations.read(locid)
        data_dict = dict(data[0])
        form.storageid.data = locid
        form.placetype.choices = place_types
        form.placetype.process_data(data_dict.get("type", None))
        form.description.data = data_dict.get("description", None)
        form.width.data = data_dict.get("width", None)
        form.depth.data = data_dict.get("depth", None)
        form.height.data = data_dict.get("height", None)
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/tool_locations/{0}/{1}'.format(storage_type, docid))
        if form.create_button.data:
            if form.create_button.label.text == "Update":
                operation = "Update"
        if form.del_button and form.del_button.data:
            operation = "Delete"
        if form.validate_on_submit():
            # Get the data from the form here
            if operation == "Create":
                try:
                    tool_location_data = {
                        "type": form_type,
                        "description": form_desc,
                        "width": form_width,
                        "depth": form_depth,
                        "height": form_height,
                    }
                    mygarage.get_session().start_transaction()
                    res = locations.create(tool_location_data)
                    last_docid = locations.get_last_docid()
                    # pylint: enable=no-member
                    if res[0]:
                        flash("Added.")
                        tool_locations = []
                        document = collection.read(docid)
                        try:
                            tool_locations.extend(document[0]['tool_locations'])
                        except KeyError:
                            pass
                        tool_locations.append(last_docid)
                        collection_data = {
                            "_id": docid,
                            "tool_locations": tool_locations
                        }
                        collection.update(collection_data)
                        mygarage.get_session().commit()
                    else:
                        flash("Cannot add tool_location: {0}".format(res[1]))
                        mygarage.get_session().rollback()
                    # pylint: disable=no-member
                    return redirect('/list/tool_locations/{0}/{1}'.format(storage_type, docid))
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    tool_location_data = {
                        "_id": locid,
                        "type": form_type,
                        "description": form_desc,
                        "width": form_width,
                        "depth": form_depth,
                        "height": form_height,
                    }
                    # pylint: disable=no-member
                    res = locations.update(tool_location_data)
                    # pylint: enable=no-member
                    if res[0]:
                        flash("Updated.")
                    else:
                        flash("Cannot update tool_location: {0}".format(res[1]))
                    return redirect('/list/tool_locations/{0}/{1}'.format(storage_type, docid))
                except Exception as err:
                    flash(err)
            else:
                try:
                    mygarage.get_session().start_transaction()
                    # pylint: disable=no-member
                    res = locations.delete(locid)
                    # pylint: enable=no-member
                    if res[0]:
                        flash("Deleted.")
                        tool_locations = []
                        document = collection.read(docid)
                        try:
                            tool_locations.extend(document[0]['tool_locations'])
                        except KeyError:
                            pass
                        tool_locations.remove(locid)
                        collection_data = {
                            "_id": docid,
                            "tool_locations": tool_locations
                        }
                        collection.update(collection_data)
                        mygarage.get_session().commit()
                    else:
                        flash("Cannot delete tool_location: {0}".format(res[1]))
                        mygarage.get_session().rollback()
                    return redirect('/list/tool_locations/{0}/{1}'.format(storage_type, docid))
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("location.html", form=form,
                           storage_place_name=storage_place_name)
# pylint: enable=too-many-locals

#
# Organizers
#
# This page allows creating and editing organizer documents.
#
# pylint: disable=too-many-locals
@app.route('/organizers', methods=['GET', 'POST'])
@app.route('/organizers/<string:organizer_id>', methods=['GET', 'POST'])
def organizer(organizer_id=None):
    """Manage organizer CRUD operations."""
    organizer_collection = Organizers(mygarage)
    tools = Tools(mygarage)
    form = OrganizerForm()
    # Get data from the form if present
    form_organizerid = form.organizerid.data
    form_type = form.organizertype.data
    form_desc = form.description.data
    form_width = form.width.data
    form_depth = form.depth.data
    form_height = form.height.data
    form_location = form.location.data
    form.location.choices = mygarage.get_locations()
    tool_list = None
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if organizer_id:
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = organizer_collection.read(organizer_id)
        if data == []:
            flash("Organizer not found!")
        data_dict = dict(data[0])
        form.organizerid.data = data_dict.get("_id", None)
        form.organizertype.process_data(data_dict.get("type", "Case"))
        form.description.data = data_dict.get("description", None)
        form.width.data = data_dict.get("width", None)
        form.depth.data = data_dict.get("depth", None)
        form.height.data = data_dict.get("height", None)
        form.location.choices = mygarage.get_locations(False)
        form.location.process_data(data_dict.get("location", None))
        tool_list = []
        tool_id_list = data_dict.get("tool_ids")
        if tool_id_list:
            for tool_id in data_dict.get("tool_ids"):
                tool_doc = tools.read(tool_id)[0]
                # only some tools have a size
                try:
                    size = tool_doc['size']
                except KeyError:
                    size = ' '
                tool_list.append((tool_id, tool_doc['type'], tool_doc['description'],
                                  tool_doc['category'], size))
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/organizers')
        if form.create_button.data:
            if form.create_button.label.text == "Update":
                operation = "Update"
        if form.del_button and form.del_button.data:
            operation = "Delete"
        if form.validate_on_submit():
            # Get the data from the form here
            if operation == "Create":
                try:
                    organizer_data = {
                        "description": form_desc,
                        "width": form_width,
                        "depth": form_depth,
                        "height": form_height,
                        "location": form_location,
                        "type": form_type,
                    }
                    res = organizer_collection.create(organizer_data)
                    if res[0]:
                        flash("Added.")
                    else:
                        flash("Cannot add organizer: {0}".format(res[1]))
                    return redirect('/list/organizers')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    organizer_data = {
                        "_id": form.organizerid.data,
                        "description": form_desc,
                        "width": form_width,
                        "depth": form_depth,
                        "height": form_height,
                        "location": form_location,
                        "type": form_type,
                    }
                    res = organizer_collection.update(organizer_data)
                    if res[0]:
                        flash("Updated.")
                    else:
                        flash("Cannot update organizer: {0}".format(res[1]))
                    return redirect('/list/organizers')
                except Exception as err:
                    flash(err)
            else:
                try:
                    res = organizer_collection.delete(form_organizerid)
                    if res[0]:
                        flash("Deleted.")
                    else:
                        flash("Cannot delete organizer: {0}".format(res[1]))
                    return redirect('/list/organizers')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("organizer.html", form=form,
                           tools=tool_list, tool_columns=TOOL_COLUMNS_ORGANIZER)

#
# Storage Places
#
# This page allows creating and editing storage places documents.
#
# pylint: disable=too-many-locals
@app.route('/storage_places/<string:kind>', methods=['GET', 'POST'])
@app.route('/storage_places/<string:kind>/<string:storage_place_id>', methods=['GET', 'POST'])
def storage_places(kind=None, storage_place_id=None):
    """Manage storage place CRUD operations."""
    if kind == 'cabinets':
        collection = Cabinets(mygarage)
        collection_str = 'Cabinet'
    elif kind == 'shelving_units':
        collection = ShelvingUnits(mygarage)
        collection_str = 'Shelving Unit'
    elif kind == 'toolchests':
        collection = Toolchests(mygarage)
        collection_str = 'Toolchest'
    elif kind == 'workbenches':
        collection = Workbenches(mygarage)
        collection_str = 'Workbench'
    elif kind == 'tools':
        # Redirect!
        flash("Must redirect to tools.")
    elif kind == 'organizers':
        # Redirect!
        flash("Must redirect to organizers.")
    else:
        flash("Something is wrong. Wrong 'kind' specified for the detail.")
    form = StoragePlaceForm()
    # Get data from the form if present
    form_storageid = form.storageid.data
    vendor_data = Vendors(mygarage)
    vendors = vendor_data.read()
    vendor_list = []
    for item in vendors:
        vendor_list.append((item["_id"], item["name"]))
    form.vendor.choices = vendor_list
    form_vendor = form.vendor.data
    form_desc = form.description.data
    # Only cabinets have doors
    if kind == 'cabinets':
        form_ndoors = form.numdoors.data
    else:
        del form.numdoors
    form_width = form.width.data
    form_depth = form.depth.data
    form_height = form.height.data
    form_location = form.location.data
    tool_locations = None
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if storage_place_id:
        if kind == 'cabinets':
            form.caption.label = "Cabinet"
        elif kind == 'shelving_units':
            form.caption.label = "Shelving Unit"
        elif kind == 'toolchests':
            form.caption.label = "Toolchest"
        elif kind == 'workbenches':
            form.caption.label = "Workbench"
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = collection.read(storage_place_id)
        if data == []:
            flash("The {0} was not found!".format(collection_str))
        data_dict = dict(data[0])
        form.vendorid.data = data_dict.get("vendorid", None)
        form.vendor.process_data(data_dict.get("vendorid", None))
        form.storageid.data = data_dict.get("_id", None)
        form.description.data = data_dict.get("description", None)
        if kind == 'cabinets':
            form.numdoors.data = data_dict.get("numdoors", None)
        form.width.data = data_dict.get("width", None)
        form.depth.data = data_dict.get("depth", None)
        form.height.data = data_dict.get("height", None)
        form.location.data = data_dict.get("location", None)
        places = data_dict.get("tool_locations")
        tool_locations = mygarage.build_storage_contents(places)
    else:
        del form.del_button
        del form.manage_tool_locations_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/{0}'.format(kind))
        if form.create_button.data:
            if form.create_button.label.text == "Update":
                operation = "Update"
        if form.del_button and form.del_button.data:
            operation = "Delete"
        if form.manage_tool_locations_button and form.manage_tool_locations_button.data:
            return redirect('/list/tool_locations/{0}/{1}'.format(kind, form.storageid.data))
        if form.validate_on_submit():
            # Get the data from the form here
            if operation == "Create":
                try:
                    storage_place_data = {
                        "vendorid": form_vendor,
                        "description": form_desc,
                        "width": form_width,
                        "depth": form_depth,
                        "height": form_height,
                        "location": form_location,
                    }
                    if kind == 'cabinets':
                        storage_place_data.update({"numdoors": form_ndoors})
                    collection.create(storage_place_data)
                    flash("Added.")
                    return redirect('/list/{0}'.format(kind))
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    storage_place_data = {
                        "_id": storage_place_id,
                        "vendorid": form_vendor,
                        "description": form_desc,
                        "width": form_width,
                        "depth": form_depth,
                        "height": form_height,
                        "location": form_location,
                    }
                    if kind == 'cabinets':
                        storage_place_data.update({"numdoors": form_ndoors})
                    collection.update(storage_place_data)
                    flash("Updated.")
                    return redirect('/list/{0}'.format(kind))
                except Exception as err:
                    flash(err)
            else:
                try:
                    mygarage.get_session().start_transaction()
                    locations = Locations(mygarage)
                    if places:
                        for loc_id in places:
                            locations.delete(loc_id)
                    collection.delete(form_storageid)
                    mygarage.get_session().commit()
                    flash("Deleted.")
                    return redirect('/list/{0}'.format(kind))
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("storage_place.html", form=form,
                           tool_locations=tool_locations,
                           tool_locations_columns=TOOL_LOCATIONS_COLUMNS)

#
# Tools
#
# This page allows creating and editing tool documents.
#
@app.route('/tools', methods=['GET', 'POST'])
@app.route('/tools/<string:tool_id>', methods=['GET', 'POST'])
def tool(tool_id=None):
    """Manage tool CRUD operations."""
    collection = Tools(mygarage)
    form = ToolForm()
    # Get data from the form if present
    form_toolid = form.toolid.data
    # Tool type choices
    vendor_data = Vendors(mygarage)
    vendors = vendor_data.read()
    vendor_list = []
    for item in vendors:
        vendor_list.append((item["_id"], item["name"]))
    form.vendor.choices = vendor_list
    form.location.choices = mygarage.get_locations()
    form_vendor = form.vendor.data
    form_desc = form.description.data
    form_location = form.location.data
    form_category = form.category.data
    form_toolsize = form.toolsize.data
    form_tooltype = form.tooltype.data
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if tool_id:
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = collection.read(tool_id)
        if data == []:
            flash("Tool not found!")
        data_dict = dict(data[0])
        form.toolid.data = data_dict.get("_id", None)
        form.vendorid.data = data_dict.get("vendorid", None)
        form.vendor.process_data(data_dict.get("vendorid", None))
        form.description.data = data_dict.get("description", None)
        form.location.choices = mygarage.get_locations()
        form.location.process_data(data_dict.get("location", None))
        form.category.process_data(data_dict.get("category", None))
        form.toolsize.data = data_dict.get("size", None)
        form.tooltype.process_data(data_dict.get("type", None))
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/tools')
        if form.create_button.data:
            if form.create_button.label.text == "Update":
                operation = "Update"
        if form.del_button and form.del_button.data:
            operation = "Delete"
        if form.validate_on_submit():
            # Get the data from the form here
            if operation == "Create":
                try:
                    tool_data = {
                        "vendorid": form_vendor,
                        "description": form_desc,
                        "type": form_tooltype,
                        "size": form_toolsize,
                        "location": form_location,
                        "category": form_category,
                    }
                    collection.create(tool_data)
                    flash("Added.")
                    return redirect('/list/tools')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    tool_data = {
                        "_id": tool_id,
                        "vendorid": form_vendor,
                        "description": form_desc,
                        "type": form_tooltype,
                        "size": form_toolsize,
                        "location": form_location,
                        "category": form_category,
                    }
                    collection.update(tool_data)
                    flash("Updated.")
                    return redirect('/list/tools')
                except Exception as err:
                    flash(err)
            else:
                try:
                    mygarage.get_session().start_transaction()
                    locations = Locations(mygarage)
                    locations.remove_tool(form_toolid)
                    organizers = Organizers(mygarage)
                    organizers.remove_tool(form_toolid)
                    collection.delete(form_toolid)
                    mygarage.get_session().commit()
                    flash("Deleted.")
                    return redirect('/list/tools')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("tool.html", form=form)
# pylint: enable=too-many-statements, too-many-locals

#
# Vendors
#
# This page allows creating and editing vendor documents.
#
# pylint: disable=too-many-nested-blocks
@app.route('/vendors', methods=['GET', 'POST'])
@app.route('/vendors/<string:vendor_id>', methods=['GET', 'POST'])
def vendor(vendor_id=None):
    """Manage vendor CRUD operations."""
    vendor_collection = Vendors(mygarage)
    form = VendorForm()
    # Get data from the form if present
    form_vendorid = form.vendorid.data
    form_name = form.name.data
    form_url = form.url.data
    form_sources = form.sources.data
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if vendor_id:
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = vendor_collection.read(vendor_id)
        if data == []:
            flash("Vendor not found!")
        data_dict = dict(data[0])
        form.vendorid.data = data_dict.get("_id", None)
        form.name.data = data_dict.get("name", None)
        form.url.data = data_dict.get("url", None)
        form.sources.data = data_dict.get("sources", None)
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/vendors')
        if form.create_button.data:
            if form.create_button.label.text == "Update":
                operation = "Update"
        if form.del_button and form.del_button.data:
            operation = "Delete"
        if form.validate_on_submit():
            # Get the data from the form here
            if operation == "Create":
                try:
                    vendor_data = {
                        "name": form_name,
                        "url": form_url,
                        "sources": form_sources,
                    }
                    res = vendor_collection.create(vendor_data)
                    if res[0]:
                        flash("Added.")
                    else:
                        flash("Cannot add vendor: {0}".format(res[1]))
                    return redirect('/list/vendors')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    vendor_data = {
                        "_id": form.vendorid.data,
                        "name": form_name,
                        "url": form_url,
                        "sources": form_sources,
                    }
                    res = vendor_collection.update(vendor_data)
                    if res[0]:
                        flash("Updated.")
                    else:
                        flash("Cannot update vendor: {0}".format(res[1]))
                    return redirect('/list/vendors')
                except Exception as err:
                    flash(err)
            else:
                try:
                    if not mygarage.vendor_in_use(form_vendorid):
                        res = vendor_collection.delete(form_vendorid)
                        if res[0]:
                            flash("Deleted.")
                        else:
                            flash("Cannot delete vendor: {0}".format(res[1]))
                    else:
                        flash("Vendor {0} in use. Cannot delete.".format(form_name))
                    return redirect('/list/vendors')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("vendor.html", form=form)
# pylint: enable=too-many-nested-blocks

#
# Error handling routes
#
@app.errorhandler(404)
def page_not_found(err):
    """Error handler"""
    print("ERROR: {0}".format(err))
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(err):
    """Error handler"""
    print("ERROR: {0}".format(err))
    return render_template('500.html'), 500

#
# Main entry
#
if __name__ == '__main__':
    #
    # Setup the program options
    #
    userid = input("User Id: ")
    passwd = getpass("Password: ")
    #
    # Setup the mygarage schema class
    #
    mygarage = MyGarage()
    mygarage.connect(userid, passwd, 'localhost', 33060)

    manager.run()
