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
from mautic.mautic.wrapper.segments import Segments
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
			frappe.log_error(e, 'Mautic Connection Error')

		if not hasattr(self.mautic_connect, 'session'):
			frappe.throw(_("Your Mautic Connection Token has expired. Please renew it."))
			frappe.log_error('Mautic Connection Token has expired', 'Mautic Integration')

	def get(self, remote_objectname, fields=None, filters=None, start=0, page_length=10):
		search = filters.get('search')

		if remote_objectname == 'Contact':
			try:
				return self.get_contacts(search, start, page_length)
			except Exception as e:
				frappe.log_error(e, 'Mautic Contact Get Error')

		if remote_objectname == 'Company':
			try:
				return self.get_companies(search, start, page_length)
			except Exception as e:
				frappe.log_error(e, 'Mautic Company Get Error')

		if remote_objectname == 'Segment':
			try:
				return self.get_segments(search, start, page_length)
			except Exception as e:
				frappe.log_error(e, 'Mautic Segment Get Error')

	def insert(self, doctype, doc):
		if doctype == 'Contact':
			if doc.reject == 1:
				return
			else:
				try:
					return self.insert_contacts(doc)
				except Exception as e:
					frappe.log_error("Doc {0}: {1}".format(doc, e), 'Mautic Contact Insert Error')

		if doctype == 'Company':
			try:
				return self.insert_companies(doc)
			except Exception as e:
				frappe.log_error("Doc {0}: {1}".format(doc, e), 'Mautic Company Insert Error')

	def update(self, doctype, doc, migration_id):
		if doctype == 'Contact':
			if doc.reject == 1:
				return
			else:
				try:
					return self.update_contacts(doc, migration_id)
				except Exception as e:
					frappe.log_error("Doc {0}: {1}".format(doc, e), 'Mautic Contact Update Error')

		if doctype == 'Company':
			try:
				return self.update_companies(doc, migration_id)
			except Exception as e:
				frappe.log_error("Doc {0}: {1}".format(doc, e), 'Mautic Company Update Error')

	def delete(self, doctype, migration_id):
		if doctype == 'Contact':
			try:
				return self.delete_contacts(migration_id)
			except Exception as e:
				frappe.log_error("Id {0}: {1}".format(migration_id, e), 'Mautic Contact Delete Error')

		if doctype == 'Company':
			try:
				return self.delete_companies(migration_id)
			except Exception as e:
				frappe.log_error("Id {0}: {1}".format(migration_id, e), 'Mautic Company Delete Error')

	def get_contacts(self, search, start=0, page_length=10):
		contacts = Contacts(client=self.mautic_connect)
		fetched_data = contacts.get_list(search=search, start=start, limit=page_length)

		if 'errors' in fetched_data:
			frappe.log_error(fetched_data['errors'], "Mautic Contact Get Error")

		else:
			result = []
			for k in fetched_data["contacts"]:
				contacts_segments = contacts.get_contact_segments(k)
				fetched_data["contacts"][k].update({'segments': contacts_segments})
				result.append(fetched_data["contacts"][k])

			return list(result)


	def get_companies(self, search, start=0, page_length=10):
		companies = Companies(client=self.mautic_connect)
		fetched_data = companies.get_list(search=search, start=start, limit=page_length)

		if 'errors' in fetched_data:
			frappe.log_error(fetched_data['errors'], "Mautic Company Get Error")

		else:
			result = []
			for k in fetched_data["companies"]:
				result.append(fetched_data["companies"][k])
			return list(result)

	def get_segments(self, search, start=0, page_length=10):
		segments = Segments(client=self.mautic_connect)
		fetched_data = segments.get_list(search=search, start=start, limit=page_length)

		if 'errors' in fetched_data:
			frappe.log_error(fetched_data['errors'], "Mautic Segment Get Error")

		else:
			result = []
			for k in fetched_data["lists"]:
				result.append(fetched_data["lists"][k])
			return list(result)

	def insert_contacts(self, doc):
		contacts = Contacts(client=self.mautic_connect)
		created_contact = contacts.create(dict(doc))

		if 'errors' in created_contact:
			frappe.log_error("Doc {0}: {1}".format(doc, created_contact['errors']), "Mautic Contact Insert Error")
		else:
			return {self.name_field: created_contact["contact"]["id"]}

	def insert_companies(self, doc):
		companies = Companies(client=self.mautic_connect)
		created_company = companies.create(dict(doc))

		if 'errors' in created_company:
			frappe.log_error("Doc {0}: {1}".format(doc, created_company['errors']), "Mautic Companies Insert Error")
		else:
			return {self.name_field: created_company["company"]["id"]}

	def update_contacts(self, doc, migration_id):
		contacts = Contacts(client=self.mautic_connect)
		updated_contact = contacts.edit(obj_id=migration_id, parameters=dict(doc), create_if_not_exists=True)

		if 'errors' in updated_contact:
			frappe.log_error("Id {0}: {1}".format(migration_id, updated_contact['errors']), "Mautic Contact Update Error")
		else:
			return {self.name_field: updated_contact["contact"]["id"]}

	def update_companies(self, doc, migration_id):
		companies = Companies(client=self.mautic_connect)
		updated_company = companies.edit(obj_id=migration_id, parameters=dict(doc), create_if_not_exists=True)

		if 'errors' in updated_company:
			frappe.log_error("Id {0}: {1}".format(migration_id, updated_company['errors']), "Mautic Company Update Error")
		else:
			return {self.name_field: updated_company["company"]["id"]}

	def delete_contacts(self, migration_id):
		contacts = Contacts(client=self.mautic_connect)
		deleted_contact = contacts.delete(obj_id=migration_id)

		if 'errors' in deleted_contact:
			if deleted_contact['errors']['code'] == 404:
				pass
			else:
				frappe.log_error("Id {0}: {1}".format(migration_id, deleted_contact['errors']), "Mautic Contact Deletion Error")
			return {self.name_field: migration_id, 'error': True}
		else:
			return {self.name_field: deleted_contact["contact"]["id"]}

	def delete_companies(self, migration_id):
		companies = Companies(client=self.mautic_connect)
		deleted_company = companies.delete(obj_id=migration_id)

		if 'errors' in deleted_company:
			if deleted_company['errors']['code'] == 404:
				pass
			else:
				frappe.log_error("Id {0}: {1}".format(migration_id, deleted_company['errors']), "Mautic Company Deletion Error")
			return {self.name_field: migration_id, 'error': True}
		else:
			return {self.name_field: deleted_company["company"]["id"]}
