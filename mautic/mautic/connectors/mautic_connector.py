from __future__ import unicode_literals
import frappe
from frappe.data_migration.doctype.data_migration_connector.connectors.base import BaseConnection
from frappe.utils.response import json_handler
from requests_oauthlib import OAuth2Session
from mautic.mautic.wrapper.api import MauticOauth2Client
import json
from frappe.utils import now_datetime
from mautic.mautic.doctype.mautic_settings.mautic_settings import refresh_token
from mautic.mautic.wrapper.contacts import Contacts
from mautic.mautic.wrapper.companies import Companies
from frappe.utils.error import make_error_snapshot

class MauticConnector(BaseConnection):
	def __init__(self, connector):
		self.connector = connector
		settings = frappe.get_doc("Mautic Settings", None)

		self.base_url = settings.base_url
		self.token = {
			'refresh_token': settings.get_password(fieldname='refresh_token',raise_exception=False),
			'access_token': settings.get_password(fieldname='session_token',raise_exception=False),
			'token_type': 'Bearer',
			'expires_in': '-30'
		}
		self.client_id = settings.client_id
		self.client_secret = settings.get_password(fieldname='client_secret',raise_exception=False)

		self.name_field = 'id'

		try:
			self.mautic_connect = MauticOauth2Client(base_url=self.base_url, client_id=self.client_id, client_secret=self.client_secret, token=self.token, token_updater=refresh_token)
		except Exception as e:
			make_error_snapshot(e)

		if not hasattr(self.mautic_connect, 'session'):
			frappe.throw(_("Your Mautic Connection Token has expired. Please renew it."))
			frappe.logger().error(' Mautic Connection Token has expired')

	def get(self, remote_objectname, fields=None, filters=None, start=0, page_length=10):
		search = filters.get('search')

		if remote_objectname == 'Contact':
			return self.get_contacts(search, start, page_length)

		if remote_objectname == 'Company':
			return self.get_companies(search, start, page_length)

	def insert(self, doctype, doc):
		if doctype == 'Contact':
			return self.insert_contacts(doc)

		if doctype == 'Company':
			return self.insert_customers(doc)

	def update(self, doctype, doc, migration_id):
		pass

	def delete(self, doctype, migration_id):
		pass

	def get_contacts(self, search, start=0, page_length=10):
		contacts = Contacts(client=self.mautic_connect)
		fetched_data = contacts.get_list(search=search, start=start, limit=page_length)

		result = []
		for k in fetched_data["contacts"]:
			result.append(fetched_data["contacts"][k])
		return list(result)

	def get_companies(self, search, start=0, page_length=10):
		companies = Companies(client=self.mautic_connect)
		fetched_data = companies.get_list(search=search, start=start, limit=page_length)

		result = []
		for k in fetched_data["companies"]:
			result.append(fetched_data["companies"][k])
		return list(result)

	def insert_contacts(self, doc):
		contacts = Contacts(client=self.mautic_connect)
		created_contact = contacts.create(dict(doc))

		return {self.name_field: created_contact["contact"]["id"]}

	def insert_customers(self, doc):
		companies = Companies(client=self.mautic_connect)
		created_company = companies.create(dict(doc))

		return {self.name_field: created_company["company"]["id"]}
