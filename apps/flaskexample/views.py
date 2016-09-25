from flask import render_template
from flask import request
from flaskexample import app
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import yaml
from a_Model import ModelIt

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
    return render_template("ny_bill_input.html", title='Home',
                           user={'nickname': 'Joel'},)


@app.route('/db')
def birth_page():
    sql_query = """
                SELECT nyb.bill_num, nyb.bill_name, ts.score
                FROM table_score as ts
                INNER JOIN ny_bills as nyb
                ON nyb.bill_num=ts.bill_num
                WHERE ts.subject='Health'
                ORDER BY ts.score DESC
                LIMIT 100;
                """
    query_results = pd.read_sql_query(sql_query, con)
    bills = ""
    print(query_results[:100])
    for i in range(0, 100):
        bills += "New York Bill "
        bills += query_results.iloc[i]['bill_num']
        bills += ': '
        bills += query_results.iloc[i]['bill_name']
        bills += "<br>"
    return bills


@app.route('/ny_bills')
def ny_bills_fancy():
    sql_query = """
    SELECT nyb.bill_num, nyb.bill_name, ts.score
    FROM table_score as ts
    INNER JOIN ny_bills as nyb
    ON nyb.bill_num=ts.bill_num
    WHERE ts.subject='Health'
    ORDER BY ts.score DESC
    LIMIT 100;
    """
    query_results = pd.read_sql_query(sql_query, con)
    bills = []
    for i in range(0, query_results.shape[0]):
        bills.append(dict(bill_num=query_results.iloc[i]['bill_num'],
                          bill_name=query_results.iloc[i]['bill_name'],
                          score=query_results.iloc[i]['score']))
    return render_template('ny_bills.html', bills=bills)


@app.route('/ny_bill_input')
def ny_bills_input():
    return render_template("ny_bill_input.html")


@app.route('/us_bill_input')
def us_bills_input():
    return render_template("us_bill_input.html")


@app.route('/ny_bills_output')
def ny_bills_output():
    # pull 'subject' from input field and store it
    subject = request.args.get('subject')
    # just select the bills for which
    # have the subject that the user inputs

    q_str = """
    SELECT nyb.bill_num, nyb.bill_name, ts.logistic
    FROM ny_score as ts
    INNER JOIN ny_bills as nyb
    ON nyb.bill_num=ts.bill_num
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

    the_result = ModelIt(subject, bills)
    return render_template("ny_bills_output.html",
                           bills=bills, the_result=the_result)


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

    the_result = ModelIt(subject, bills)
    return render_template("us_bills_output.html",
                           bills=bills, the_result=the_result)


@app.route('/lda_topics')
def lda_topics():
    return render_template("lda_vis.html")
