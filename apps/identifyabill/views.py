from flask import render_template
from flask import request
from identifyabill import app
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import yaml
from identifyabill.support_functions import formatted_query

ymlfile = open("../configs.yml", 'r')
cfg = yaml.load(ymlfile)
ymlfile.close()

dbname = cfg['dbname']
user = cfg['username']
host = 'localhost'
db = create_engine('postgres://%s%s/%s' % (user, host, dbname))
con = None
con = psycopg2.connect(database=dbname, user=user)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Identifyabill.site',
                           user={'nickname': 'Joel'},)


@app.route('/us_bill_input')
def us_bills_input():
    return render_template("us_bill_input.html")


@app.route('/results')
def ny_bills_output():
    # pull 'subject' from input field and store it
    subject = request.args.get('subject')
    offset = request.args.get('offset')
    if (offset is None or int(offset) < 0):
        offset = 0
    limit = 20
    # just select the bills for which
    # have the subject that the user inputs

    score_col = cfg['score_column']
    q_str = """
    SELECT nyb.bill_num, nyb.bill_name, ts.{0}
    FROM ny_score as ts
    INNER JOIN ny_bills as nyb
    ON nyb.bill_num=ts.bill_num
    WHERE ts.subject={1}
    AND ts.{0} IS NOT NULL
    ORDER BY ts.{0} DESC
    LIMIT {2}
    OFFSET {3}
    """
    q_fill = q_str.format(score_col, subject, limit, offset)
    query_results = pd.read_sql_query(q_fill, con)

    bills = formatted_query(query_results, score_col)
    # bills = []
    # for i in range(0, query_results.shape[0]):
    #    bills.append(dict(bill_num=query_results.iloc[i]['bill_num'],
    #                      bill_name=query_results.iloc[i]['bill_name'],
    #                      score=query_results.iloc[i]['logistic']))

    conversion_dict = {"'Health'": 'Health', "'Taxation'": 'Taxation',
                       "'Competition_and_antitrust'": 'Antitrust',
                       "'Employee_benefits_and_pensions'": 'Employee Benefits',
                       "'Bankruptcy'": 'Bankruptcy',
                       "'Intellectual_property'": 'Intellectual Property',
                       "'Labor_and_employment'": 'Labor and Employment',
                       "'Securities'": 'Securities',
                       "'Bank_accounts_deposits_and_capital'": 'Banking'}
    return render_template("results.html", bills=bills, cdict=conversion_dict,
                           subject=subject, offset=offset)


@app.route('/us_bills_output')
def us_bills_output():
    # pull 'subject' from input field and store it
    subject = request.args.get('subject')
    # just select the bills for which
    # have the subject that the user inputs

    q_str = """
    SELECT usb.bill_num, usb.bill_name, ts.logistic
    FROM us_score as ts
    INNER JOIN us_bills as usb
    ON usb.bill_num=ts.bill_num
    WHERE ts.subject={0}
    AND ts.logistic IS NOT NULL
    ORDER BY ts.logistic DESC
    LIMIT 100;
    """
    q_fill = q_str.format(subject)
    query_results = pd.read_sql_query(q_fill, con)

    bills = []
    for i in range(0, query_results.shape[0]):
        bills.append(dict(bill_num=query_results.iloc[i]['bill_num'],
                          bill_name=query_results.iloc[i]['bill_name'],
                          score=query_results.iloc[i]['logistic']))

    return render_template("us_bills_output.html", bills=bills)


@app.route('/lda_topics')
def lda_topics():
    return render_template("lda_vis.html")
