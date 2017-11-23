# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "mautic_integration"
app_title = "Mautic Integration"
app_publisher = "DOKOS"
app_description = "Synchronizes Mautic with ERPNext"
app_icon = "octicon octicon-git-compare"
app_color = "#f5f5f5"
app_email = "hello@dokos.io"
app_license = "GPLv3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mautic_integration/css/mautic_integration.css"
# app_include_js = "/assets/mautic_integration/js/mautic_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/mautic_integration/css/mautic_integration.css"
# web_include_js = "/assets/mautic_integration/js/mautic_integration.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "mautic_integration.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "mautic_integration.install.before_install"
# after_install = "mautic_integration.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mautic_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mautic_integration.tasks.all"
# 	],
# 	"daily": [
# 		"mautic_integration.tasks.daily"
# 	],
# 	"hourly": [
# 		"mautic_integration.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mautic_integration.tasks.weekly"
# 	]
# 	"monthly": [
# 		"mautic_integration.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "mautic_integration.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mautic_integration.event.get_events"
# }
