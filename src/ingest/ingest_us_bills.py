from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import os
import datetime
from bills.ingest.setup_database import US_Bill
from bills.ingest.setup_database import Bill_Subject


def get_latest_text_dir(path):
    latest_date = datetime.datetime(1900, 1, 1)
    dir_name = ""
    for status_dir in os.listdir(path):
        status_file = path + '/' + status_dir + '/data.json'
        with open(status_file) as data_file:
            status_data = json.load(data_file)
            date = datetime.datetime.strptime(status_data['issued_on'],
                                              '%Y-%m-%d')
            if (date > latest_date):
                latest_date = date
                dir_name = status_dir

    return dir_name


def extract_us_bills(dbname='bills_db', username='Joel',
                     bills_dir='/Users/Joel/Desktop/Insight/data/bills'):

    engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

    # Open a session and connect to the database engine
    Session = sessionmaker(bind=engine)
    session = Session()

    for bill_type_dir in os.listdir(bills_dir):
        type_dir = bills_dir + '/' + bill_type_dir
        for bill_dir in os.listdir(type_dir):
            bill_path = type_dir + '/' + bill_dir

            text_dir_base = bill_path + '/text-versions'
            if (os.path.isdir(text_dir_base)):
                dir_name = get_latest_text_dir(text_dir_base)
                text_name = text_dir_base + '/' + dir_name + '/document.txt'

                text = ""
                with open(text_name) as text_file:
                    text = text_file.readlines()

                outer_json = bill_path + '/' + 'data.json'
                with open(outer_json) as data_file:
                    bill_data = json.load(data_file)
                    bill_num = bill_data['bill_id']
                    bill_name = bill_data['official_title']
                    top_subject = bill_data['subjects_top_term']
                    one_bill = US_Bill(bill_num=bill_num, bill_name=bill_name,
                                       bill_text=text, top_subject=top_subject)
                    session.add(one_bill)

                    for term in bill_data['subjects']:
                        one_sub = Bill_Subject(bill_num=bill_num, subject=term)
                        session.add(one_sub)

    session.commit()
    session.close()
