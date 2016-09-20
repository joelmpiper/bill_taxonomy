#!/Users/Joel/anaconda/envs/insight/bin/python
# coding: utf-8

# ### Need to loop over all of the legislation (10,000s) by 1,000 at a time. Extract the bill IDs, and then extract the bill text one-by-one. After retrieving the bill text, store it to a database on AWS with some associated metadata.
#
# ### Then, I will need to figure out how to do that for the U.S. Congress. Use the U.S. Congress bill text as the training data, with the given subject terms, and use that to train. See how well that predicts other bills in the U.S. congress and use that model for the New York legislation. Go through a subset of the new york data and see if there are keywords or other information that can be used to hand label. Also, use the given terms to use as a broader base of keywords for labeling the U.S. data. Also, try running in an unsupervised setting to see how the data clusters.

# In[1]:

import requests
my_key = open('/Users/Joel/Documents/insight/ny_bill_keys.txt', 'r').readline().strip()


# In[2]:

import time


# In[3]:

# Set up the database to save the results of the new york bill table
# There will be one table for the New York bills and one for U.S. bills
## Python packages - you may have to pip install sqlalchemy, sqlalchemy_utils, and psycopg2.
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd


# In[4]:

#In Python: Define a database name
dbname = 'bills_db'
username = 'Joel'
## 'engine' is a connection to a database
## Here, we're using postgres, but sqlalchemy can connect to other things too.
engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))
print engine.url

## create a database (if it doesn't exist)
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))


# In[5]:

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# In[6]:

from sqlalchemy import Column, Integer, String
class New_York_Bill(Base):
    __tablename__ = 'ny_bills'
    bill_num = Column(String, primary_key=True)
    bill_name = Column(String)
    bill_text = Column(String)

    def __repr__(self):
        return "<New_York_Bill(bill_num='%s', bill_name='%s', bill_text='%s')>" % (
            self.bill_num, self.bill_name, self.bill_text)


# In[7]:

ny_bills_table = New_York_Bill.__table__


# In[8]:

# Actually create the table
Base.metadata.create_all(engine)


# In[9]:

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


# In[10]:

#ny_bills_table.drop(engine)
# This seems painful. Drop the table from the command line before running the command below.


# In[10]:

#requests.get('http://legislation.nysenate.gov/api/3/bills/2015/A02257?view=only_fullText&key=' + my_key).json()


# In[ ]:

# Run through a loop getting files 1,000 at a time until we receive all files
offset = 0
year = 2015
limit = 1000
#limit = 10
key = my_key
my_max = 50000
#my_max = 50
request_string = 'http://legislation.nysenate.gov/api/3/bills/{0}?limit={1}&offset={2}&key={3}'.format(year,
                                                                                                        limit,
                                                                                                        offset,
                                                                                                        key)
all_bills = requests.get(request_string).json()

while ((all_bills['responseType'] == 'bill-info list') and offset < my_max):
    print all_bills['offsetStart']
    offset += limit
    request_string = 'http://legislation.nysenate.gov/api/3/bills/{0}?limit={1}&offset={2}&key={3}'.format(year,
                                                                                                        limit,
                                                                                                        offset,
                                                                                                        key)
    all_bills = requests.get(request_string).json()

    if (all_bills['responseType'] == 'bill-info list'):
        for bill in all_bills['result']['items']:
            bill_num = bill['printNo']
            single_request = 'http://legislation.nysenate.gov/api/3/bills/{0}/{1}?view=only_fullText&key={2}'.format(
            year, bill_num, my_key)
            bill_data = requests.get(single_request).json()
            bill_text = bill_data['result']['fullText']
            #print bill_num
            #print bill['title']
            #print bill
            one_bill = New_York_Bill(bill_num=bill_num, bill_name=bill['title'], bill_text=bill_text)
            session.add(one_bill)
            time.sleep(1)

    time.sleep(2)
    session.commit()

session.commit()


# In[ ]:

from sqlalchemy import text
result = session.query(New_York_Bill).from_statement(text("SELECT * FROM ny_bills"))


# In[13]:

all_bills = result.all()


# In[14]:

len(all_bills)


# In[22]:

all_bills[0]


# In[16]:

all_bills[-1]


# In[17]:

session.close()

