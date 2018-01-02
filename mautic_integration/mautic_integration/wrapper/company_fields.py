# -*- coding: utf-8 -*-
# Initial code by https://github.com/divio/python-mautic 
from __future__ import unicode_literals, absolute_import

from .api import API


class CompanyFields(API):
    _endpoint = 'fields/company'
