from __future__ import unicode_literals
import frappe
from frappe.data_migration.doctype.data_migration_connector.connectors.base import BaseConnection
from frappe.utils.response import json_handler
from requests_oauthlib import OAuth2Session
from mautic_integration.mautic_integration.wrapper.api import MauticOauth2Client
import json
from frappe.utils import now_datetime
from mautic_integration.mautic_integration.doctype.mautic_settings.mautic_settings import refresh_token

class Mautic(BaseConnection):
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

	def get(self, remote_objectname, fields=None, filters=None, start=0, page_length=10):
		search = filters.get('search')

		if remote_objectname == 'Contact':
			return self.get_contacts(search, start, page_length)

		if remote_objectname == 'Company':
			return self.get_companies(search, start, page_length)

	def insert(self, doctype, doc):
		pass

	def update(self, doctype, doc, migration_id):
		pass

	def delete(self, doctype, migration_id):
		pass

	def get_contacts(self, search, start=0, page_length=10):
		from mautic_integration.mautic_integration.wrapper.contacts import Contacts

		mautic = MauticOauth2Client(base_url=self.base_url, client_id=self.client_id, client_secret=self.client_secret, token=self.token, token_updater=refresh_token)

		contacts = Contacts(client=mautic)
		fetched_data = contacts.get_list(search=search, start=start, limit=page_length)
		print(fetched_data["contacts"])

		result = []
		for k in fetched_data["contacts"]:
			print(k)
			result.append(fetched_data["contacts"][k])
		return list(result)

	def get_companies(self, search, start=0, page_length=10):
		from mautic_integration.mautic_integration.wrapper.companies import Companies

		mautic = MauticOauth2Client(base_url=self.base_url, client_id=self.client_id, client_secret=self.client_secret, token=self.token, token_updater=refresh_token)

		companies = Companies(client=mautic)
		fetched_data = companies.get_list(search=search, start=start, limit=page_length)
		print(fetched_data["companies"])

		result = []
		for k in fetched_data["companies"]:
			print(k)
			result.append(fetched_data["companies"][k])
		return list(result)
