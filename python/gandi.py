#!/usr/bin/python3
# 
# The MIT License (MIT)
# Copyright (c) 2016 Jean-Daniel Fischer
# 
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the “Software”), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
# 
# The Software is provided “as is”, without warranty of any kind, express 
# or implied, including but not limited to the warranties of merchantability, 
# fitness for a particular purpose and noninfringement. In no event shall 
# the authors or copyright holders be liable for any claim, damages or other 
# liability, whether in an action of contract, tort or otherwise, arising from, 
# out of or in connection with the software or the use or other dealings in the Software.
# 

import logging
from xmlrpc.client import ServerProxy

class GandiApiException(Exception):
    """
    Use to hold an error message.
    """

    def __init__(self, message):
        self._message = message

    def get_message(self):
        return self._message


class ZoneUpdater(object):
    """
    Clone the active zone and updates server name ip.
    """

    def __init__(self, api_key, api_url):
        """
        server_name: dns entry
        new_ip: new ip of dns entry
        api_key: gandi valid api key
        api_url: gandi valid api url
        """
        self._api_key = api_key
        self._api_url = api_url
        self._api = ServerProxy(api_url)

    def update_zone(self, zone_name, record_name, new_ip):
        """
        zone_name: zone name with a dot at the end
        record_name: dns entry
        new_ip: new ip of dns entry
        """
        logging.info('Start update zone %s, record %s' % (zone_name, record_name))
        self._clone_zone(zone_name)
        self._update_record(record_name, new_ip)
        self._activate_new_zone()
        logging.info('End update zone %s, record %s' % (zone_name, record_name))

    def _clone_zone(self, zone_name):
        """
        Use API to access the current zone and prepare the next one.
        Set self._current_zone and self._new_zone_version_number.
        """
        list_zone = self._api.domain.zone.list(self._api_key)
        for zone in list_zone:
            if zone['name'] == zone_name:
                self._current_zone = zone
        if not self._current_zone:
            raise ApiGandiException('Failed to find zone %s' % (zone_name))
        
        self._new_zone_version_number = self._api.domain.zone.version.new(self._api_key, self._current_zone['id'])
        if not self._new_zone_version_number:
            raise ApiGandiException('Failed to get new zone version number for zone %s' % (zone_name))
        logging.info('Find zone %s' % (zone_name))

    def _update_record(self, record_name, ip):
        """
        Update a given record (the short name for exemple a.b.c in zone b.c. as record_name equal to a)
        to a specific ip.
        """
        if (not self._current_zone) or (not self._new_zone_version_number):
            raise ApiGandiException("Can't update record, no cloned zone available")
        
        list_record =  self._api.domain.zone.record.list(self._api_key, self._current_zone['id'], 
            self._new_zone_version_number)
        for record in list_record:
            if record['name'] == record_name:
                myrecord = record
        # Create new record
        self._api.domain.zone.record.update(self._api_key, self._current_zone['id'], 
            self._new_zone_version_number, {'id': myrecord['id']}, 
            {
            'name': myrecord['name'],
            'type': myrecord['type'],
            'value': ip,
            'ttl': myrecord['ttl']
            })
        logging.info('Update record %s with ip %s successfully' % (record_name, ip))

    def _activate_new_zone(self):
        """
        Set new zone has the active one.
        """
        if (not self._current_zone) or (not self._new_zone_version_number):
            raise ApiGandiException("Can't update record, no cloned zone available")
        success = self._api.domain.zone.version.set(self._api_key, self._current_zone['id'], 
            self._new_zone_version_number)
        if not success:
            raise ApiGandiException('Failed to activate new zone')
        else:
            logging.info('New zone version activated')
