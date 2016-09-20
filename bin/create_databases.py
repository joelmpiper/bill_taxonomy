#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" create-databases
 Create all databases for the bill taxonomy project if they do not already
 exist.

 Author:   Joel Piper <joelmpiper [at] gmail.com>
 Created: Saturday, September 19, 2016

"""

# Imports
import sys
from src.ingest.setup_database import make_database


def main(*argv):

    print(make_database())

if __name__ == '__main__':
    main(*sys.argv)
