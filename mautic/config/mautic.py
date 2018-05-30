# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Settings"),
			"items": [
				{
					"type": "doctype",
					"name": "Mautic Settings",
					"description": _("Mautic Settings"),
				}
				]
		},
		{
			"label": _("Documents"),
			"items": [
				{
					"type": "doctype",
					"name": "Mautic Segment",
					"description": _("Mautic Segment"),
				}
				]
		}
	]
