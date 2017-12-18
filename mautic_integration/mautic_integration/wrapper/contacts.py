# -*- coding: utf-8 -*-
# Initial code by https://github.com/divio/python-mautic 
from __future__ import unicode_literals, absolute_import

from .api import API


class Contacts(API):
    # Contact unsubscribed themselves.
    UNSUBSCRIBED = 1
    # Contact was unsubscribed due to an unsuccessful send.
    BOUNCED = 2
    # Contact was manually unsubscribed by user.
    MANUAL = 3

    _endpoint = 'contacts'

    def get_owners(self):
        """
        Get a list of users available as contact owners
        :return: dict|str
        """
        response = self._client.session.get(
            '{url}/list/owners'.format(url=self.endpoint_url)
        )
        return self.process_response(response)

    def get_field_list(self):
        """
        Get a list of custom fields
        :return: dict|str
        """
        response = self._client.session.get(
            '{url}/list/fields'.format(url=self.endpoint_url)
        )
        return self.process_response(response)

    def get_segments(self):
        """
        Get a list of contact segments
        :return: dict|str
        """
        response = self._client.session.get(
            '{url}/list/segments'.format(url=self.endpoint_url)
        )
        return self.process_response(response)

    def get_events(
        self,
        obj_id,
        search='',
        include_events=None,
        exclude_events=None,
        order_by='',
        order_by_dir='ASC',
        page=1
    ):
        """
        Get a list of a contact's engagement events
        :param obj_id: int Contact ID
        :param search: str
        :param include_events: list|tuple
        :param exclude_events: list|tuple
        :param order_by: str
        :param order_by_dir: str
        :param page: int
        :return: dict|str
        """
        if include_events is None:
            include_events = []
        if exclude_events is None:
            exclude_events = []

        parameters = {
            'search': search,
            'includeEvents': include_events,
            'excludeEvents': exclude_events,
            'orderBy': order_by,
            'orderByDir': order_by_dir,
            'page': page
        }
        response = self._client.session.get(
            '{url}/{id}/events'.format(
                url=self.endpoint_url, id=obj_id
            ),
            params=parameters
        )
        return self.process_response(response)

    def get_contact_notes(
        self,
        obj_id,
        search='',
        start=0,
        limit=0,
        order_by='',
        order_by_dir='ASC'
    ):
        """
        Get a list of a contact's notes
        :param obj_id: int Contact ID
        :param search: str
        :param start: int
        :param limit: int
        :param order_by: str
        :param order_by_dir: str
        :return: dict|str
        """

        parameters = {
            'search': search,
            'start': start,
            'limit': limit,
            'orderBy': order_by,
            'orderByDir': order_by_dir,
        }
        response = self._client.session.get(
            '{url}/{id}/notes'.format(
                url=self.endpoint_url, id=obj_id
            ),
            params=parameters
        )
        return self.process_response(response)

    def get_contact_segments(self, obj_id):
        """
        Get a segment of smart segments the contact is in
        :param obj_id: int
        :return: dict|str
        """

        response = self._client.session.get(
            '{url}/{id}/segments'.format(
                url=self.endpoint_url, id=obj_id
            )
        )
        return self.process_response(response)

    def get_contact_campaigns(self, obj_id):
        """
        Get a segment of campaigns the contact is in
        :param obj_id: int
        :return: dict|str
        """

        response = self._client.session.get(
            '{url}/{id}/campaigns'.format(
                url=self.endpoint_url, id=obj_id
            )
        )
        return self.process_response(response)

    def add_points(self, obj_id, points, **kwargs):
        """
        Add the points to a contact
        :param obj_id: int
        :param points: int
        :param kwargs: dict 'eventname' and 'actionname'
        :return: dict|str
        """

        response = self._client.session.post(
            '{url}/{id}/points/plus/{points}'.format(
                url=self.endpoint_url, id=obj_id, points=points
            ),
            data=kwargs
        )
        return self.process_response(response)

    def subtract_points(self, obj_id, points, **kwargs):
        """
        Subtract points from a contact
        :param obj_id: int
        :param points: int
        :param kwargs: dict 'eventname' and 'actionname'
        :return: dict|str
        """

        response = self._client.session.post(
            '{url}/{id}/points/minus/{points}'.format(
                url=self.endpoint_url, id=obj_id, points=points
            ),
            data=kwargs
        )
        return self.process_response(response)

    def add_dnc(
        self,
        obj_id,
        channel='email',
        reason=MANUAL,
        channel_id=None,
        comments='via API'
    ):
        """
        Adds Do Not Contact
        :param obj_id: int
        :param channel: str
        :param reason: str
        :param channel_id: int
        :param comments: str
        :return: dict|str
        """
        data = {
            'reason': reason,
            'channelId': channel_id,
            'comments': comments
        }
        response = self._client.session.post(
            '{url}/{id}/dnc/add/{channel}'.format(
                url=self.endpoint_url, id=obj_id, channel=channel
            ),
            data=data
        )
        return self.process_response(response)

    def remove_dnc(self, obj_id, channel):
        """
        Removes Do Not Contact
        :param obj_id: int
        :param channel: str
        :return: dict|str
        """
        response = self._client.session.post(
            '{url}/{id}/dnc/remove/{channel}'.format(
                url=self.endpoint_url, id=obj_id, channel=channel
            )
        )
        return self.process_response(response)
