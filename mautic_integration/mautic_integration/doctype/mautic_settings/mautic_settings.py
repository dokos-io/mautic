# -*- coding: utf-8 -*-
# Copyright (c) 2017, DOKOS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import get_request_site_address, now_datetime
import requests
from frappe.utils.response import json_handler
import urllib
import datetime

class MauticSettings(Document):
	pass

@frappe.whitelist()
def authorization_code():
	doc = frappe.get_doc("Mautic Settings")
	data = {
		'client_id': doc.client_id,
		'client_secret': doc.get_password(fieldname='client_secret',raise_exception=False),
		'redirect_uri': get_request_site_address(True) + '?cmd=mautic_integration.mautic_integration.doctype.mautic_settings.mautic_settings.mautic_callback',
		'grant_type': 'authorization_code',
		'response_type': 'code'
		}
	url = doc.base_url + '/oauth/v2/authorize?' + urllib.urlencode(data)

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
					'redirect_uri': get_request_site_address(True) + '?cmd=mautic_integration.mautic_integration.doctype.mautic_settings.mautic_settings.mautic_callback',
					'code': code,
					'grant_type': 'authorization_code'
					}
			r = requests.post(doc.base_url + '/oauth/v2/token', data=data).json()
			if 'refresh_token' in r:
				frappe.db.set_value("Mautic Settings", None, "refresh_token", r['refresh_token'])
			if 'access_token' in r:
				frappe.db.set_value("Mautic Settings", None, "session_token", r['access_token'])
			frappe.db.commit()
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
