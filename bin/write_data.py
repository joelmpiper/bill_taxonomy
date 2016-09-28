#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" write_data
Fill in missing data for a subject when the model is available in
pickle format.

 Author:   Joel Piper <joelmpiper [at] gmail.com>
 Created: Saturday, September 27, 2016

"""

# Imports
import sys
import yaml

from src.ingest.get_bills import get_us_bills
from src.ingest.get_bills import get_ny_bills
from src.ingest.get_bills import get_subjects
from src.wrangle.create_features import make_x_values
from src.wrangle.create_features import make_y_values
from src.analyze.run_model import get_y_probs
from src.report.store_db import store_us_db
from src.report.store_db import store_ny_db
import pickle


def main(*argv):
    with open("write_data.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

        dbname = cfg['dbname']
        username = cfg['username']
        sub = cfg['subject']
        us_bills = get_us_bills(dbname, username, 50000)
        subjects = get_subjects(dbname, username, [sub])
        X = make_x_values(us_bills)

        y = make_y_values(us_bills, subjects, sub)
        fit_mod = pickle.load(open(cfg['model_dir'] + '/' + cfg['file_name']))
        if(cfg['store_us']):
            y_probs_us = get_y_probs(fit_mod, X, cfg)
            store_us_db(dbname, us_bills, sub, y_probs_us, y, cfg)

        if(cfg['store_ny']):
            ny_bills = get_ny_bills(dbname, username, 50000)
            X_ny = make_x_values(ny_bills)
            y_probs_ny = get_y_probs(fit_mod, X_ny, cfg)
            store_ny_db(dbname, ny_bills, sub, y_probs_ny, cfg)

        return 0

if __name__ == '__main__':
    main(*sys.argv)
