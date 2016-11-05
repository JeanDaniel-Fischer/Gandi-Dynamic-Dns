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
from socket import gethostbyname
from urllib.request import urlopen

class IpChecker(object):
    """
    Collect dns value and current internet ip to identify mismatch.
    """

    def __init__(self, hostname):
        self.host = hostname
        self._get_reference_ip()
        self._get_current_ip()


    def _get_reference_ip(self):
        """
        Do a dns request to get current ip
        """
        # TODO use getaddrinfo for support IPV6
        self._reference_ip = gethostbyname(self.host)
        logging.debug('IPv4 from dns is "%s" for %s' % 
              (self._reference_ip, self.host))

    def _get_current_ip(self):
        """
        Get current internet ip from external service api.ipify.org.
        Raise URLError when it failed to reach api.
        """
        with urlopen(url='https://api.ipify.org') as webpage:
            for line in webpage:
                self._current_ip = bytes.decode(line)
        logging.debug('IPv4 from external is "%s"' % 
              (self._current_ip))

    def is_match_external_dns(self):
        """
        True if dns ip and external ip matches.
        """
        return self._current_ip == self._reference_ip

    def get_new_ip(self):
        return self._current_ip
