#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe

def pre_process(companies):
	return {
		'id': companies["id"],
		'companyname': companies["fields"]["all"]["companyname"],
		'companywebsite': companies["fields"]["all"]["companywebsite"]
	}

def post_process(remote_doc=None, local_doc=None, **kwargs):
	if not local_doc:
		return

	customer = local_doc
	country = remote_doc["fields"]["all"]["companycountry"]
	if country is not None:
		if not frappe.db.exists("Country", country):
			frappe.get_doc({
				'doctype': 'Country',
				'country_name': country
			}).insert(ignore_permissions=True)

		seq = (customer.name, "Mautic")
		address_name = "-".join(seq)

		if not frappe.db.exists("Address", address_name):
			address = frappe.get_doc({
				'doctype': 'Address',
				'address_title': remote_doc["fields"]["all"]["companyname"],
				'address_line1': remote_doc["fields"]["all"]["companyaddress1"],
				'address_line2': remote_doc["fields"]["all"]["companyaddress2"],
				'city': remote_doc["fields"]["all"]["companycity"],
				'pincode': remote_doc["fields"]["all"]["companyzipcode"],
				'state': remote_doc["fields"]["all"]["companystate"],
				'country': country,
				'email_id': remote_doc["fields"]["all"]["companyemail"],
				'phone': remote_doc["fields"]["all"]["companyphone"],
				'links': [{
					'link_doctype': 'Customer',
					'link_name': customer.name
				}]
			}).insert(ignore_permissions=True)
			frappe.db.commit()

			address.name = address_name
			address.insert(ignore_permissions=True)

		else:
			address = frappe.get_doc('Address', address_name)
			address.address_title = remote_doc["fields"]["all"]["companyname"]
			address.address_line1 = remote_doc["fields"]["all"]["companyaddress1"]
			address.address_line2 = remote_doc["fields"]["all"]["companyaddress2"]
			address.city = remote_doc["fields"]["all"]["companycity"]
			address.pincode = remote_doc["fields"]["all"]["companyzipcode"]
			address.state = remote_doc["fields"]["all"]["companystate"]
			address.country = country
			address.email_id = remote_doc["fields"]["all"]["companyemail"]
			address.phone = remote_doc["fields"]["all"]["companyphone"]
			address.save()

		frappe.db.commit()

	else:
		return
