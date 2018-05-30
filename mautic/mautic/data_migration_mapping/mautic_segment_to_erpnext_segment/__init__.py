#!/usr/bin/env python
# -*- coding: utf-8 -*-
import frappe

def pre_process(segments):
	return {
		'id': segments["id"],
		'name': segments["name"],
		'description': segments["description"]
	}
