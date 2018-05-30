# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from .api import API


class Segments(API):
	_endpoint = 'segments'

	def add_contact(self, segment_id, contact_id):
		"""
		Add a contact to the segment
		:param segment_id: int Segment ID
		:param contact_id: int Contact ID
		:return: dict|str
		"""

		response = self._client.session.post(
			'{url}/{segment_id}/contact/{contact_id}/add'.format(
				url=self.endpoint_url,
				segment_id=segment_id,
				contact_id=contact_id
			)
		)
		return self.process_response(response)


	def remove_contact(self, segment_id, contact_id):
		"""
		Removes a contact from the segment
		:param segment_id: int Segment ID
		:param contact_id: int Contact ID
		:return: dict|str
		"""

		response = self._client.session.post(
			'{url}/{segment_id}/contact/{contact_id}/remove'.format(
				url=self.endpoint_url,
				segment_id=segment_id,
				contact_id=contact_id
			)
		)
		return self.process_response(response)
