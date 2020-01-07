#
# Introducing the MySQL Shell - MyGarage Version 1
#
# This file contains the sample Python + Flask application for demonstrating
# how to build a simple relational database application. Thus, it relies on
# a database class that encapsulates the CRUD operations for a MySQL database
# of relational tables.
#
# Dr. Charles Bell, 2019
#
""" MyGarage Flask Application Version 1"""
from __future__ import print_function

from getpass import getpass
from flask import Flask, render_template, request, redirect, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import (HiddenField, TextField, SelectField, IntegerField, SubmitField)
from wtforms.validators import Required, Length

from database.garage_v1 import MyGarage
from database.handtool import Handtool, HANDTOOL_TYPES
from database.location import Location
from database.organizer import Organizer, ORGANIZER_TYPES
from database.place import Place, PLACE_TYPES
from database.powertool import Powertool, POWERTOOL_TYPES
from database.storage import Storage, STORAGE_TYPES
from database.vendor import Vendor

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

class HandtoolForm(FlaskForm):
    """Handtool form class"""
    handtoolid = HiddenField('Id')
    vendor = NewSelectField(
        'Vendor', validators=[Required(message=REQUIRED.format("Vendor"))]
    )
    description = TextField(
        'Description',
        validators=[Required(message=REQUIRED.format("Description")),
                    Length(min=1, max=125, message=RANGE.format("Description", 1, 125))]
    )
    handtooltype = NewSelectField(
        'Handtool Type',
        validators=[Required(message=REQUIRED.format("Handtool Type"))]
    )
    toolsize = TextField('ToolSize')
    place = NewSelectField(
        'Location',
        validators=[Required(message=REQUIRED.format("Location"))]
    )
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    close_button = SubmitField('Close')

class OrganizerForm(FlaskForm):
    """Organizer form class"""
    organizerid = HiddenField('Id')
    place = NewSelectField(
        'Location',
        validators=[Required(message=REQUIRED.format("Location"))]
    )
    organizertype = NewSelectField(
        'OrganizerType',
        validators=[Required(message=REQUIRED.format("OragnizerType"))]
    )
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

class PlaceForm(FlaskForm):
    """Place form class"""
    placeid = HiddenField('Id')
    storage = NewSelectField(
        'Storage',
        validators=[Required(message=REQUIRED.format("Storage"))]
    )
    placetype = NewSelectField(
        'PlaceType',
        validators=[Required(message=REQUIRED.format("PlaceType"))]
    )
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

class PowertoolForm(FlaskForm):
    """Powertool form class"""
    powertoolid = HiddenField('Id')
    vendor = NewSelectField(
        'Vendor',
        validators=[Required(message=REQUIRED.format("Vendor"))]
    )
    description = TextField(
        'Description',
        validators=[Required(message=REQUIRED.format("Description")),
                    Length(min=1, max=125, message=RANGE.format("Description", 1, 125))]
    )
    powertooltype = NewSelectField(
        'Powertool Type',
        validators=[Required(message=REQUIRED.format("Powertool Type"))]
    )
    place = NewSelectField(
        'Location',
        validators=[Required(message=REQUIRED.format("Location"))]
    )
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    close_button = SubmitField('Close')

class StorageForm(FlaskForm):
    """Storage form class"""
    storageid = HiddenField('Id')
    vendor = NewSelectField(
        'Vendor',
        validators=[Required(message=REQUIRED.format("Vendor"))]
    )
    storagetype = NewSelectField(
        'StorageType',
        validators=[Required(message=REQUIRED.format("StorageType"))]
    )
    description = TextField(
        'Description',
        validators=[Required(message=REQUIRED.format("Description")),
                    Length(min=1, max=125, message=RANGE.format("Description", 1, 125))]
    )
    numdrawers = IntegerField('Num Drawers')
    numshelves = IntegerField('Num Shelves')
    numdoors = IntegerField('Num Doors')
    width = IntegerField('Width')
    depth = IntegerField('Depth')
    height = IntegerField('Height')
    location = TextField(
        'Location',
        validators=[Required(message=REQUIRED.format("Location")),
                    Length(min=1, max=40, message=RANGE.format("Location", 1, 40))]
    )
    create_button = SubmitField('Add')
    del_button = SubmitField('Delete')
    close_button = SubmitField('Close')

class VendorForm(FlaskForm):
    """Vendor form class"""
    vendorid = HiddenField('VendorId')
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
# template "list.html" to show a list of rows from the database. Built into
# each row is a special edit link for editing any of the rows, which redirects
# to the appropriate route (form).
#
# pylint: disable=too-many-return-statements
@app.route('/', methods=['GET', 'POST'])
@app.route('/list/<kind>', methods=['GET', 'POST'])
def simple_list(kind=None):
    """Display the simple list and landing page"""
    rows = []
    columns = []
    form = ListForm()
    if kind == 'handtool':
        form.form_name.label = 'Handtools'
        if request.method == 'POST':
            return redirect('handtool')
        columns = (
            '<td style="width:100px"><b>ToolType</b></td>',
            '<td style="width:200px"><b>Description</b></td>',
            '<td style="width:200px"><b>Tool Size/Application</b></td>',
            '<td style="width:400px"><b>Storage Equipment</b></td>',
            '<td style="width:200px"><b>Location Type</b></td>',
            '<td style="width:200px"><b>Location</b></td>',
        )
        kind = 'handtool'
        handtool_data = Handtool(mygarage)
        rows = handtool_data.read()
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    elif kind == 'organizer':
        form.form_name.label = 'Organizers'
        if request.method == 'POST':
            return redirect('organizer')
        columns = (
            '<td style="width:100px"><b>Type</b></td>',
            '<td style="width:300px"><b>Description</b></td>',
            '<td style="width:400px"><b>Storage Equipment</b></td>',
            '<td style="width:200px"><b>Location Type</b></td>',
            '<td style="width:200px"><b>Location</b></td>',
        )
        kind = 'organizer'
        organizer_data = Organizer(mygarage)
        rows = organizer_data.read()
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    elif kind == 'powertool':
        form.form_name.label = 'Powertools'
        if request.method == 'POST':
            return redirect('powertool')
        columns = (
            '<td style="width:100px"><b>ToolType</b></td>',
            '<td style="width:500px"><b>Description</b></td>',
            '<td style="width:200px"><b>Storage Equipment</b></td>',
            '<td style="width:200px"><b>Location Type</b></td>',
            '<td style="width:200px"><b>Location</b></td>',
        )
        kind = 'powertool'
        powertool_data = Powertool(mygarage)
        rows = powertool_data.read()
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    elif kind == 'place':
        form.form_name.label = 'Storage Places'
        if request.method == 'POST':
            return redirect('place')
        columns = (
            '<td style="width:500px"><b>Storage Equipment</b></td>',
            '<td style="width:100px"><b>Location Type</b></td>',
            '<td style="width:200px"><b>Location</b></td>',
        )
        kind = 'place'
        place_data = Place(mygarage)
        rows = place_data.read()
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    elif kind == 'storage' or not kind:
        form.form_name.label = 'Storage Equipment'
        if request.method == 'POST':
            return redirect('storage')
        columns = (
            '<td style="width:100px"><b>Vendor</b></td>',
            '<td style="width:100px"><b>Type</b></td>',
            '<td style="width:500px"><b>Description</b></td>',
            '<td style="width:300px"><b>Location</b></td>',
        )
        kind = 'storage'
        storage_data = Storage(mygarage)
        rows = storage_data.read(brief=True)
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    elif kind == 'vendor':
        form.form_name.label = 'Vendors'
        if request.method == 'POST':
            return redirect('vendor')
        columns = (
            '<td style="width:200px"><b>Name</b></td>',
            '<td style="width:400px"><b>URL</b></td>',
            '<td style="width:200px"><b>Sources</b></td>',
        )
        kind = 'vendor'
        vendor_data = Vendor(mygarage)
        rows = vendor_data.read()
        return render_template("list.html", form=form, rows=rows,
                               columns=columns, kind=kind)
    else:
        flash("Something is wrong. No 'kind' specified for list!")
        return None
# pylint: enable=too-many-return-statements

#
# Handtool
#
# This page allows creating and editing handtool records.
#
@app.route('/handtool', methods=['GET', 'POST'])
@app.route('/handtool/<int:handtool_id>', methods=['GET', 'POST'])
def handtool(handtool_id=None):
    """Manage handtool CRUD operations."""
    handtool_table = Handtool(mygarage)
    form = HandtoolForm()
    # Get data from the form if present
    form_handtoolid = form.handtoolid.data
    # Handtool type chocies
    form.handtooltype.choices = HANDTOOL_TYPES
    vendor_list = Vendor(mygarage)
    vendors = vendor_list.read()
    vendor_list = []
    for item in vendors:
        vendor_list.append((item[0], '{0}'.format(item[1])))
    form.vendor.choices = vendor_list
    form_vendor = form.vendor.data
    storage_list = Location(mygarage)
    places = storage_list.read()
    place_list = []
    for item in places:
        place_list.append((item[0], '{0} - {1}, {2}'.format(item[1], item[2],
                                                            item[3])))
    form.place.choices = place_list
    form_place = form.place.data
    form_handtooltype = form.handtooltype.data
    form_desc = form.description.data
    form_toolsize = form.toolsize.data
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if handtool_id:
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = handtool_table.read(handtool_id)
        if data == []:
            flash("Handtool not found!")
        form.handtoolid.data = data[0][0]
        form.vendor.process_data(data[0][1])
        form.description.data = data[0][2]
        form.handtooltype.process_data(data[0][3])
        form.toolsize.data = data[0][4]
        form.place.process_data(data[0][5])
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/handtool')
        if form.create_button.data:
            if form.create_button.label.text == "Update":
                operation = "Update"
        if form.del_button and form.del_button.data:
            operation = "Delete"
        if form.validate_on_submit():
            # Get the data from the form here
            if operation == "Create":
                try:
                    handtool_data = {
                        "VendorId": form_vendor,
                        "Description": form_desc,
                        "Type": form_handtooltype,
                        "ToolSize": form_toolsize,
                        "PlaceId": form_place
                    }
                    handtool_table.create(handtool_data)
                    flash("Added.")
                    return redirect('/list/handtool')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    handtool_data = {
                        "HandtoolId": handtool_id,
                        "VendorId": form_vendor,
                        "Description": form_desc,
                        "Type": form_handtooltype,
                        "ToolSize": form_toolsize,
                        "PlaceId": form_place
                    }
                    handtool_table.update(handtool_data)
                    flash("Updated.")
                    return redirect('/list/handtool')
                except Exception as err:
                    flash(err)
            else:
                try:
                    handtool_table.delete(form_handtoolid)
                    flash("Deleted.")
                    return redirect('/list/handtool')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("handtool.html", form=form)

#
# Organizer
#
# This page allows creating and editing organizer records.
#
@app.route('/organizer', methods=['GET', 'POST'])
@app.route('/organizer/<int:organizer_id>', methods=['GET', 'POST'])
def organizer(organizer_id=None):
    """Manage organize CRUD operations."""
    organizer_table = Organizer(mygarage)
    form = OrganizerForm()
    # Get data from the form if present
    form_organizerid = form.organizerid.data
    # Organizer type chocies
    form.organizertype.choices = ORGANIZER_TYPES
    storage_list = Location(mygarage)
    places = storage_list.read()
    place_list = []
    for item in places:
        place_list.append((item[0], '{0} - {1}, {2}'.format(item[1], item[2],
                                                            item[3])))
    form.place.choices = place_list
    form_place = form.place.data
    form_organizertype = form.organizertype.data
    form_desc = form.description.data
    form_width = form.width.data
    form_depth = form.depth.data
    form_height = form.height.data
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if organizer_id:
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = organizer_table.read(organizer_id)
        if data == []:
            flash("Organizer not found!")
        form.organizerid.data = data[0][0]
        form.place.process_data(data[0][1])
        form.organizertype.process_data(data[0][2])
        form.description.data = data[0][3]
        form.width.data = data[0][4]
        form.depth.data = data[0][5]
        form.height.data = data[0][6]
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/organizer')
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
                        "PlaceId": form_place,
                        "Type": form_organizertype,
                        "Description": form_desc,
                        "Width": form_width,
                        "Depth": form_depth,
                        "Height": form_height,
                    }
                    organizer_table.create(organizer_data)
                    flash("Added.")
                    return redirect('/list/organizer')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    organizer_data = {
                        "OrganizerId": organizer_id,
                        "PlaceId": form_place,
                        "Type": form_organizertype,
                        "Description": form_desc,
                        "Width": form_width,
                        "Depth": form_depth,
                        "Height": form_height,
                    }
                    organizer_table.update(organizer_data)
                    flash("Updated.")
                    return redirect('/list/organizer')
                except Exception as err:
                    flash(err)
            else:
                try:
                    organizer_table.delete(form_organizerid)
                    flash("Deleted.")
                    return redirect('/list/organizer')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("organizer.html", form=form)

#
# Place
#
# This page allows creating and editing place records.
#
@app.route('/place', methods=['GET', 'POST'])
@app.route('/place/<int:place_id>', methods=['GET', 'POST'])
def place(place_id=None):
    """Manage place CRUD operations."""
    place_table = Place(mygarage)
    form = PlaceForm()
    # Get data from the form if present
    form_placeid = form.placeid.data
    # Place type chocies
    form.placetype.choices = PLACE_TYPES
    storage_list = Storage(mygarage)
    storages = storage_list.read()
    storage_list = []
    for item in storages:
        storage_list.append((item[0], '{0}'.format(item[3])))
    form.storage.choices = storage_list
    form_storage = form.storage.data
    form_placetype = form.placetype.data
    form_desc = form.description.data
    form_width = form.width.data
    form_depth = form.depth.data
    form_height = form.height.data
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if place_id:
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = place_table.read(place_id)
        if data == []:
            flash("Place not found!")
        form.placeid.data = data[0][0]
        form.storage.process_data(data[0][1])
        form.placetype.process_data(data[0][2])
        form.description.data = data[0][3]
        form.width.data = data[0][4]
        form.depth.data = data[0][5]
        form.height.data = data[0][6]
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/place')
        if form.create_button.data:
            if form.create_button.label.text == "Update":
                operation = "Update"
        if form.del_button and form.del_button.data:
            operation = "Delete"
        if form.validate_on_submit():
            # Get the data from the form here
            if operation == "Create":
                try:
                    place_data = {
                        "StorageId": form_storage,
                        "Type": form_placetype,
                        "Description": form_desc,
                        "Width": form_width,
                        "Depth": form_depth,
                        "Height": form_height,
                    }
                    place_table.create(place_data)
                    flash("Added.")
                    return redirect('/list/place')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    place_data = {
                        "PlaceId": place_id,
                        "StorageId": form_storage,
                        "Type": form_placetype,
                        "Description": form_desc,
                        "Width": form_width,
                        "Depth": form_depth,
                        "Height": form_height,
                    }
                    place_table.update(place_data)
                    flash("Updated.")
                    return redirect('/list/place')
                except Exception as err:
                    flash(err)
            else:
                try:
                    place_table.delete(form_placeid)
                    flash("Deleted.")
                    return redirect('/list/place')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("place.html", form=form)

#
# Powertool
#
# This page allows creating and editing powertool records.
#
@app.route('/powertool', methods=['GET', 'POST'])
@app.route('/powertool/<int:powertool_id>', methods=['GET', 'POST'])
def powertool(powertool_id=None):
    """Manage powertool CRUD operations."""
    powertool_table = Powertool(mygarage)
    form = PowertoolForm()
    # Get data from the form if present
    form_powertoolid = form.powertoolid.data
    # Powertool type chocies
    form.powertooltype.choices = POWERTOOL_TYPES
    vendor_data = Vendor(mygarage)
    vendors = vendor_data.read()
    vendor_list = []
    for item in vendors:
        vendor_list.append((item[0], '{0}'.format(item[1])))
    form.vendor.choices = vendor_list
    form_vendor = form.vendor.data
    storage_data = Location(mygarage)
    places = storage_data.read()
    place_list = []
    for item in places:
        place_list.append((item[0], '{0} - {1}, {2}'.format(item[1], item[2],
                                                            item[3])))
    form.place.choices = place_list
    form_place = form.place.data
    form_powertooltype = form.powertooltype.data
    form_desc = form.description.data
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if powertool_id:
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = powertool_table.read(powertool_id)
        if data == []:
            flash("Powertool not found!")
        form.powertoolid.data = data[0][0]
        form.vendor.process_data(data[0][1])
        form.description.data = data[0][2]
        form.powertooltype.process_data(data[0][3])
        form.place.process_data(data[0][4])
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/powertool')
        if form.create_button.data:
            if form.create_button.label.text == "Update":
                operation = "Update"
        if form.del_button and form.del_button.data:
            operation = "Delete"
        if form.validate_on_submit():
            # Get the data from the form here
            if operation == "Create":
                try:
                    powertool_data = {
                        "VendorId": form_vendor,
                        "Description": form_desc,
                        "Type": form_powertooltype,
                        "PlaceId": form_place
                    }
                    powertool_table.create(powertool_data)
                    flash("Added.")
                    return redirect('/list/powertool')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    powertool_data = {
                        "PowertoolId": powertool_id,
                        "VendorId": form_vendor,
                        "Description": form_desc,
                        "Type": form_powertooltype,
                        "PlaceId": form_place
                    }
                    powertool_table.update(powertool_data)
                    flash("Updated.")
                    return redirect('/list/powertool')
                except Exception as err:
                    flash(err)
            else:
                try:
                    powertool_table.delete(form_powertoolid)
                    flash("Deleted.")
                    return redirect('/list/powertool')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("powertool.html", form=form)


#
# Storage
#
# This page allows creating and editing storage records.
#
# pylint: disable=too-many-locals
@app.route('/storage', methods=['GET', 'POST'])
@app.route('/storage/<int:storage_id>', methods=['GET', 'POST'])
def storage(storage_id=None):
    """Manage storage CRUD operations."""
    storage_table = Storage(mygarage)
    form = StorageForm()
    # Get data from the form if present
    form_storageid = form.storageid.data
    # Storage type chocies
    form.storagetype.choices = STORAGE_TYPES
    vendor_data = Vendor(mygarage)
    vendors = vendor_data.read()
    vendor_list = []
    for item in vendors:
        vendor_list.append((item[0], '{0}'.format(item[1])))
    form.vendor.choices = vendor_list
    form_vendor = form.vendor.data
    form_storagetype = form.storagetype.data
    form_desc = form.description.data
    form_ndrawers = form.numdrawers.data
    form_nshelves = form.numshelves.data
    form_ndoors = form.numdoors.data
    form_width = form.width.data
    form_depth = form.depth.data
    form_height = form.height.data
    form_location = form.location.data
    # If the route with the variable is called, change the create button to update
    # then populate the form with the data from the row in the table. Otherwise,
    # remove the delete button because this will be a new data item.
    if storage_id:
        form.create_button.label.text = "Update"
        # Here, we get the data and populate the form
        data = storage_table.read(storage_id)
        if data == []:
            flash("Storage not found!")
        form.storageid.data = data[0][0]
        form.vendor.process_data(data[0][1])
        form.storagetype.process_data(data[0][2])
        form.description.data = data[0][3]
        form.numdrawers.data = data[0][4]
        form.numshelves.data = data[0][5]
        form.numdoors.data = data[0][6]
        form.width.data = data[0][7]
        form.depth.data = data[0][8]
        form.height.data = data[0][9]
        form.location.data = data[0][10]
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/storage')
        if form.create_button.data:
            if form.create_button.label.text == "Update":
                operation = "Update"
        if form.del_button and form.del_button.data:
            operation = "Delete"
        if form.validate_on_submit():
            # Get the data from the form here
            if operation == "Create":
                try:
                    storage_data = {
                        "VendorId": form_vendor,
                        "StorageType": form_storagetype,
                        "Description": form_desc,
                        "NumDrawers": form_ndrawers,
                        "NumShelves": form_nshelves,
                        "NumDoors": form_ndoors,
                        "Width": form_width,
                        "Depth": form_depth,
                        "Height": form_height,
                        "Location": form_location,
                    }
                    storage_table.create(storage_data)
                    flash("Added.")
                    return redirect('/list/storage')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    storage_data = {
                        "StorageId": storage_id,
                        "VendorId": form_vendor,
                        "StorageType": form_storagetype,
                        "Description": form_desc,
                        "NumDrawers": form_ndrawers,
                        "NumShelves": form_nshelves,
                        "NumDoors": form_ndoors,
                        "Width": form_width,
                        "Depth": form_depth,
                        "Height": form_height,
                        "Location": form_location,
                    }
                    storage_table.update(storage_data)
                    flash("Updated.")
                    return redirect('/list/storage')
                except Exception as err:
                    flash(err)
            else:
                try:
                    storage_table.delete(form_storageid)
                    flash("Deleted.")
                    return redirect('/list/storage')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("storage.html", form=form)
# pylint: enable=too-many-locals

#
# Vendor
#
# This page allows creating and editing vendor records.
#
@app.route('/vendor', methods=['GET', 'POST'])
@app.route('/vendor/<int:vendor_id>', methods=['GET', 'POST'])
def vendor(vendor_id=None):
    """Manage vendor CRUD operations."""
    vendor_table = Vendor(mygarage)
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
        data = vendor_table.read(vendor_id)
        if data == []:
            flash("Vendor not found!")
        form.vendorid.data = data[0][0]
        form.name.data = data[0][1]
        form.url.data = data[0][2]
        form.sources.data = data[0][3]
    else:
        del form.del_button
    if request.method == 'POST':
        # First, determine if we must create, update, or delete when form posts.
        operation = "Create"
        if form.close_button.data:
            return redirect('/list/vendor')
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
                        "Name": form_name,
                        "URL": form_url,
                        "Sources": form_sources,
                    }
                    res = vendor_table.create(vendor_data)
                    if res[0]:
                        flash("Added.")
                    else:
                        flash("Cannot add vendor: {0}".format(res[1]))
                    return redirect('/list/vendor')
                except Exception as err:
                    flash(err)
            elif operation == "Update":
                try:
                    vendor_data = {
                        "VendorId": form.vendorid.data,
                        "Name": form_name,
                        "URL": form_url,
                        "Sources": form_sources,
                    }
                    res = vendor_table.update(vendor_data)
                    if res[0]:
                        flash("Updated.")
                    else:
                        flash("Cannot update vendor: {0}".format(res[1]))
                    return redirect('/list/vendor')
                except Exception as err:
                    flash(err)
            else:
                try:
                    res = vendor_table.delete(form_vendorid)
                    if res[0]:
                        flash("Deleted.")
                    else:
                        flash("Cannot delete vendor: {0}".format(res[1]))
                    return redirect('/list/vendor')
                except Exception as err:
                    flash(err)
        else:
            flash_errors(form)
    return render_template("vendor.html", form=form)

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
    # Setup the mygarage database class
    #
    mygarage = MyGarage()
    mygarage.connect(userid, passwd, 'localhost', 33060)

    manager.run()
