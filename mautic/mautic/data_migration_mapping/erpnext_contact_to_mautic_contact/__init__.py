#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe

def pre_process(doc):
	company = None
	reject = None
	try:
		for link in doc.links:
			if link.link_doctype == "Customer":
				company = link.link_name
			elif link.link_doctype not in ["Customer", "Lead"]:
				reject = 1
	except:
		return doc

	if doc.email_id=="Guest":
		reject = 1

	returned_doc = {
		'first_name': doc.first_name,
		'last_name': doc.last_name,
		'email_id': doc.email_id,
		'salutation': doc.salutation,
		'phone': doc.phone,
		'mobile_no': doc.mobile_no,
		'company': company,
		'mautic_sync_id': doc.mautic_sync_id,
		'reject': reject
	}

	return returned_doc
