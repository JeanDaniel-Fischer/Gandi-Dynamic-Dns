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
import requests

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

    def update_zone(self, zone_name, record_name, new_ip):
        """
        zone_name: zone name with a dot at the end
        record_name: dns entry
        new_ip: new ip of dns entry
        """
        logging.info('Start update zone %s, record %s' % (zone_name, record_name))
        zone_name = zone_name[0:len(zone_name) - 1] if zone_name[len(zone_name) - 1] == '.' else zone_name
        self._update_record(zone_name, record_name, new_ip)
        logging.info('End update zone %s, record %s' % (zone_name, record_name))

    def _update_record(self, zone_name, record_name, ip):
        """
        Update a given record (the short name for exemple a.b.c in zone b.c. as record_name equal to a)
        to a specific ip.
        """
        
        r = requests.put('%slivedns/domains/%s/records/%s/A' % (self._api_url, zone_name, record_name),
                         json={'rrset_values': [ip], 'rrset_ttl': 300},
                         headers= {'Authorization': 'Bearer %s' % self._api_key})
        
        print(r.url)
        print(r.headers)
        if r.status_code >= 400:
            raise GandiApiException('Failed to update record %s' % (r.text))
        
        logging.info('Update record %s with ip %s successfully.' % (record_name, ip))
