import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import time
from bills.ingest.setup_database import New_York_Bill


# Retrieve the bill number, title, and text for the New York Legislature
def extractNyBills(dbname='bills_db', username='Joel',
                   offset=0, year=2015, limit=1000, my_max=50000):

    engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

    # Open a session and connect to the database engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # Get the key to access the site
    my_key = open('/Users/Joel/Documents/' + 'insight/ny_bill_keys.txt',
                  'r').readline().strip()

    # Run through a loop getting files 1,000 at a time until we receive
    # all files

    request_string = 'http://legislation.nysenate.gov/api/3/' + \
        'bills/{0}?limit={1}&offset={2}&key={3}'.format(year, limit, offset,
                                                        my_key)

    all_bills = requests.get(request_string).json()

    while ((all_bills['responseType'] == 'bill-info list') and offset < my_max):

        offset += limit
        request_string = 'http://legislation.nysenate.gov/api/3' + \
            '/bills/{0}?limit={1}&offset={2}&key={3}'.format(year, limit,
                                                             offset, my_key)
        all_bills = requests.get(request_string).json()

        if (all_bills['responseType'] == 'bill-info list'):
            for bill in all_bills['result']['items']:
                bill_num = bill['printNo']
                single_request = 'http://legislation.nysenate.gov/api/3/' + \
                    'bills/{0}/{1}?view=only_fullText&key={2}'.format(year,
                                                                      bill_num,
                                                                      my_key)
                bill_data = requests.get(single_request).json()
                bill_text = bill_data['result']['fullText']

                one_bill = New_York_Bill(bill_num=bill_num,
                                         bill_name=bill['title'],
                                         bill_text=bill_text)
                session.add(one_bill)
                time.sleep(1)

        time.sleep(2)
        session.commit()

    session.commit()
