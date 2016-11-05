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
import os

class ParamLoader(object):
    """
    Use to load param from environment or one line file.
    """

    def __init__(self, env_name):
        """
        env_name is the environment variable and file name in lower case.
        """
        try:
            self._value = os.environ[env_name]
        except KeyError:
            logging.info('Do not find in env %s' % env_name)
            self._value = None
        
        if not self._value:
            logging.debug('Unable to find %s from environment, trying from file' %(env_name))
            try:
                with open(env_name.lower(), 'r') as file:
                    self._value = file.readline().rstrip('\n').rstrip('\r')
            except OSError as error:
                logging.debug('Unable to find from file either')

    def get_value(self):
        """
        Access the value of the param, None if not found.
        """
        return self._value

