# -*- coding: utf-8 -*-
# Copyright (c) 2017, DOKOS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import get_request_site_address, now_datetime
import requests
from frappe.utils.response import json_handler
from six.moves.urllib.parse import urlencode
import datetime

if frappe.conf.developer_mode:
	import os
	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

class MauticSettings(Document):
	def validate(self):
		if self.enable == 1:
			self.create_mautic_connector()
			self.create_mautic_plan()

	def sync(self):
		"""Create and execute Data Migration Run for Mautic Sync plan"""
		frappe.has_permission('Mautic Settings', throw=True)

		exists = frappe.db.exists('Data Migration Run', dict(status=('in', ['Fail', 'Error']),	name=('!=', self.name)))
		if exists:
			failed_run = frappe.get_doc("Data Migration Run", dict(status=('in', ['Fail', 'Error'])))
			failed_run.delete()

		started = frappe.db.exists('Data Migration Run', dict(status=('in', ['Started']),	name=('!=', self.name)))
		if started:
			print("Break")
			return

		try:
			doc = frappe.get_doc({
				'doctype': 'Data Migration Run',
				'data_migration_plan': 'Mautic Sync',
				'data_migration_connector': 'Mautic Connector'
			}).insert()

			try:
				doc.run()
			except Exception:
					frappe.log_error(frappe.get_traceback())
		except Exception as e:
			frappe.logger().debug({"Mautic Error: "}, e)

	def create_mautic_connector(self):
		if frappe.db.exists('Data Migration Connector', 'Mautic Connector'):
			mautic_connector = frappe.get_doc('Data Migration Connector', 'Mautic Connector')
			mautic_connector.connector_type = 'Custom'
			mautic_connector.python_module = 'mautic.mautic.connectors.mautic_connector'
			mautic_connector.save()
			return

		frappe.get_doc({
			'doctype': 'Data Migration Connector',
			'connector_type': 'Custom',
			'connector_name': 'Mautic Connector',
			'python_module': 'mautic.mautic.connectors.mautic_connector',
		}).insert()

	def create_mautic_plan(self):
		if frappe.db.exists('Data Migration Plan', 'Mautic Sync'):
			mautic_sync = frappe.get_doc('Data Migration Plan', 'Mautic Sync')
			mautic_sync.module = "Mautic"
			mautic_sync.update({"mappings":[]})

			mappings = ["Mautic Segment to ERPNext Segment", "Mautic Company to ERPNext Customer", "Mautic Contact to ERPNext Contact", 
			"ERPNext Customer to Mautic Companies", "ERPNext Contact to Mautic Contact", "Mautic Segments"]

			for mapping in mappings:
				if mapping == "Mautic Segments":
					mautic_sync.append("mappings", {
						"mapping": mapping,
						"enabled": 0
					})
				else:
					mautic_sync.append("mappings", {
						"mapping": mapping,
						"enabled": 1
					})
			mautic_sync.save()
			frappe.db.commit()
			return

		else:
			mautic_sync = frappe.get_doc('Data Migration Plan', 'Mautic Sync')
			mautic_sync.module = "Mautic"

			mappings = ["Mautic Segment to ERPNext Segment", "Mautic Company to ERPNext Customer", "Mautic Contact to ERPNext Contact", 
			"ERPNext Customer to Mautic Companies", "ERPNext Contact to Mautic Contact", "Mautic Segments"]

			for mapping in mappings:
				if mapping == "Mautic Segments":
					mautic_sync.append("mappings", {
						"mapping": mapping,
						"enabled": 0
					})
				else:
					mautic_sync.append("mappings", {
						"mapping": mapping,
						"enabled": 1
					})
			mautic_sync.insert()

@frappe.whitelist()
def sync():
	mautic_settings = frappe.get_doc('Mautic Settings')
	if mautic_settings.enable == 1:
		if not frappe.db.exists('Data Migration Connector', 'Mautic Connector'):
			self.create_mautic_connector()
		if not frappe.db.exists('Data Migration Plan', 'Mautic Sync'):
			self.create_mautic_plan()
		try:
			mautic_settings.sync()
		except Exception:
			frappe.log_error(frappe.get_traceback())



@frappe.whitelist()
def authorization_code():
	doc = frappe.get_doc("Mautic Settings")
	data = {
		'client_id': doc.client_id,
		'client_secret': doc.get_password(fieldname='client_secret',raise_exception=False),
		'redirect_uri': get_request_site_address(True) + '?cmd=mautic.mautic.doctype.mautic_settings.mautic_settings.mautic_callback',
		'grant_type': 'authorization_code',
		'response_type': 'code'
		}
	url = doc.base_url + '/oauth/v2/authorize?' + urlencode(data)

	return url

@frappe.whitelist()
def mautic_callback(code=None):
	doc = frappe.get_doc("Mautic Settings")
	if code is None:
		pass
	else:
		frappe.db.set_value("Mautic Settings", None, "authorization_code", code)
		try:
			data = {'client_id': doc.client_id,
					'client_secret': doc.get_password(fieldname='client_secret',raise_exception=False),
					'redirect_uri': get_request_site_address(True) + '?cmd=mautic.mautic.doctype.mautic_settings.mautic_settings.mautic_callback',
					'code': code,
					'grant_type': 'authorization_code'
					}
			r = requests.post(doc.base_url + '/oauth/v2/token', data=data).json()
			if 'refresh_token' in r:
				frappe.db.set_value("Mautic Settings", None, "refresh_token", r['refresh_token'])
			if 'access_token' in r:
				frappe.db.set_value("Mautic Settings", None, "session_token", r['access_token'])
			frappe.db.commit()
			frappe.local.response["type"] = "redirect"
			frappe.local.response["location"] = "/success.html"
			return

		except Exception as e:
			frappe.throw(e.message)

@frappe.whitelist()
def refresh_token(token):
	if 'refresh_token' in token:
		frappe.db.set_value("Mautic Settings", None, "refresh_token", token['refresh_token'])
	if 'access_token' in token:
		frappe.db.set_value("Mautic Settings", None, "session_token", token['access_token'])
	frappe.db.commit()
