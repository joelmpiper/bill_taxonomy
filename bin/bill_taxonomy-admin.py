#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" solar-admin
 An administrative script for bill taxonomy information

 Author:   Joel Piper <joelmpiper [at] gmail.com>
 Created: Saturday, September 12, 2016

"""

# Imports
import sys
from bills.analyze.model import get_us_data


def main(*argv):

    print(get_us_data())

if __name__ == '__main__':
    main(*sys.argv)
