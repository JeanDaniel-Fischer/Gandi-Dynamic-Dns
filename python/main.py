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
from urllib.error import URLError
from ipchecker import IpChecker
from params import ParamLoader
from gandi import GandiApiException, ZoneUpdater

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s~>%(message)s', 
        datefmt='%m/%d/%Y-%I:%M:%S', 
        level=logging.INFO)
    try:
        zone_param = ParamLoader('ZONE')
        record_param = ParamLoader('RECORD')
        ipchecker = IpChecker(record_param.get_value() + '.' + zone_param.get_value())

        if not ipchecker.is_match_external_dns():
            api_key_param = ParamLoader('API_KEY')
            api_url_param = ParamLoader('API_URL')
            zone_updater = ZoneUpdater(api_key_param.get_value(), api_url_param.get_value())
            zone_updater.update_zone(zone_param.get_value(), record_param.get_value(), ipchecker.get_new_ip())
        else:
            logging.info('Nothing to do')
    except URLError as urle:
        logging.error('Unable to determine current external ip')
    except GandiApiException as gandi_exp:
        logging.error('Failed to update gandi: %s' % (gandi_exp.get_message()))
