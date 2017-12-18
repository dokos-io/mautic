# -*- coding: utf-8 -*-
# Initial code by https://github.com/divio/python-mautic 
from __future__ import unicode_literals, absolute_import

from .api import API


class Companies(API):
    _endpoint = 'companies'

    def add_contact(self, obj_id, contact_id):
        """
        Add a contact to the company
        :param obj_id: int Company ID
        :param contact_id: int Contact ID
        :return: dict|str
        """
        response = self._client.session.post(
            '{url}/{id}/contact/add/{contact_id}'.format(
                url=self.endpoint_url, id=obj_id, contact_id=contact_id
            )
        )
        return self.process_response(response)

    def remove_contact(self, obj_id, contact_id):
        """
        Remove a contact from the company
        :param obj_id: int Campaign ID
        :param contact_id: int Contact ID
        :return: dict|str
        """
        response = self._client.session.post(
            '{url}/{id}/contact/remove/{contact_id}'.format(
                url=self.endpoint_url, id=obj_id, contact_id=contact_id
            )
        )
        return self.process_response(response)
