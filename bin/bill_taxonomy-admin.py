#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" bill_taxonomy-admin
 An administrative script for bill taxonomy information

 Author:   Joel Piper <joelmpiper [at] gmail.com>
 Created: Saturday, September 12, 2016

"""

# Imports
import sys
import yaml

from src.ingest.get_bills import get_us_bills
from src.ingest.get_bills import get_ny_bills
from src.ingest.get_bills import get_subjects
from src.wrangle.create_features import make_feat_union
from src.analyze.run_model import create_model
from src.analyze.run_model import run_model
from src.wrangle.create_features import make_x_values
from src.wrangle.create_features import make_y_values
from src.analyze.run_model import get_y_probs
from src.report.store_db import store_us_db
from src.report.store_db import store_ny_db


def main(*argv):
    with open("configs.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

        dbname = cfg['dbname']
        username = cfg['username']
        us_bills_subset = cfg['us_bills_subset']
        subject_list = cfg['subjects']
        pipe_feats = cfg['pipe_feats']
        model_type = cfg['model_type']
        us_bills = get_us_bills(dbname, username, us_bills_subset)
        subjects = get_subjects(dbname, username, subject_list)
        X = make_x_values(us_bills)
        feat_un, feat_params = make_feat_union(pipe_feats, cfg)
        model = create_model(feat_un, model_type, feat_params, cfg)

        results = []
        for sub in subject_list:
            y = make_y_values(us_bills, subjects, sub)
            fit_mod = run_model(model, X, y, sub, cfg)
            results.append(fit_mod)

            if(cfg['store_us']):
                y_probs_us = get_y_probs(fit_mod, X)
                store_us_db(dbname, us_bills, sub, y_probs_us, y, cfg)

            if(cfg['store_ny']):
                ny_bills_subset = cfg['ny_bills_subset']
                ny_bills = get_ny_bills(dbname, username, ny_bills_subset)
                X_ny = make_x_values(ny_bills)
                y_probs_ny = get_y_probs(fit_mod, X_ny)
                store_ny_db(dbname, ny_bills, sub, y_probs_ny, cfg)

        return results

if __name__ == '__main__':
    main(*sys.argv)
