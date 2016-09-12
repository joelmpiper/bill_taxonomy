from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

# create the base class for the tables
Base = declarative_base()

dbname = 'bills_db'
username = 'Joel'


# create a class for the New York Bill table
class New_York_Bill(Base):
    __tablename__ = 'ny_bills'
    bill_num = Column(String, primary_key=True)
    bill_name = Column(String)
    bill_text = Column(String)

    def __repr__(self):
        return "<New_York_Bill(bill_num='%s', bill_name='%s', bill_text='%s')>"\
            % (self.bill_num, self.bill_name, self.bill_text)


class US_Bill(Base):
    __tablename__ = 'us_bills'
    bill_num = Column(String, primary_key=True)
    bill_name = Column(String)
    bill_text = Column(String)
    top_subject = Column(String)

    def __repr__(self):
        return "<US_Bill(bill_num='%s', bill_name='%s', bill_text='%s,'," + \
            "top_subject='%s,')>" % (self.bill_num, self.bill_name,
                                     self.bill_text, self.top_subject)

class Bill_Subject(Base):
    __tablename__ = 'bill_subject'
    bill_num = Column(String, primary_key=True)
    subject = Column(String, primary_key=True)

    def __repr__(self):
        return "<Bill_Subject(bill_num='%s', subject='%s')>" % (
            self.bill_num, self.subject)


# Setup the database
def make_database():

    engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

    # create a database (if it doesn't exist)
    if not database_exists(engine.url):
        create_database(engine.url)

    # Actually create the table
    Base.metadata.create_all(engine)
