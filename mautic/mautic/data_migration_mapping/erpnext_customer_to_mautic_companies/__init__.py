#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe
import json

def post_process(remote_doc=None, local_doc=None, **kwargs):
	if 'error' in remote_doc:
		data = local_doc
		data.pop('mautic_sync_id')
		frappe.db.set_value("Deleted Document", dict(deleted_name=local_doc['name']), "data", json.dumps(data))