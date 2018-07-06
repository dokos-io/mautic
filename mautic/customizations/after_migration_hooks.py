# Copyright (c) 2018, DOKOS and Contributors

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
import os
import json

def customization_data(filename):
	folder = frappe.get_app_path('mautic', 'mautic', 'custom')

	if os.path.exists(folder):
		for fname in os.listdir(folder):
			if fname == filename:
				with open(os.path.join(folder, fname), 'r') as f:
					data = json.loads(f.read())

					return data

def contact_custom():
	if not frappe.db.exists("Custom Field", dict(dt="Contact", fieldname="mautic_segments")):
		data = customization_data('contact.json')

		for customization in data['custom_fields']:
			frappe.set_user("Administrator")
			create_custom_field('Contact', frappe._dict(customization))

def check_custom_fields():
	contact_custom()

def after_migrate():
	check_custom_fields()