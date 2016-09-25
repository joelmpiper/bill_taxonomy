from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import yaml

# create the base class for the tables
Base = declarative_base()


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


class Subject_Score(Base):
    __tablename__ = 'table_score'
    subject = Column(String, primary_key=True)
    bill_num = Column(String, primary_key=True)
    score = Column(Float)
    logistic = Column(Float)

    def __repr__(self):
        ret_string = ("<Subject_Score(subject={0}, bill_num={1}, score={2}, "
                      "logistic={3})>")
        return ret_string.format(self.subject, self.bill_num, self.score,
                                 self.logistic)


class Subject_Logistic_Score(Base):
    __tablename__ = 'subject_logistic_score'
    subject = Column(String, primary_key=True)
    bill_num = Column(String, primary_key=True)
    score = Column(Float)

    def __repr__(self):
        return ("<Subject_Logistic_Score(subject='%s', bill_num='%s'," +
                " score='%d')>" % (self.subject, self.bill_num, self.score))


class US_Score(Base):
    __tablename__ = 'us_score'
    subject = Column(String, primary_key=True)
    bill_num = Column(String, primary_key=True)
    actual = Column(Boolean)
    score = Column(Float)
    logistic = Column(Float)

    def __repr__(self):
        ret_string = ("<US_Score(subject={0}, bill_num={1}, score={2}, "
                      "logistic={3}, actual={4})>")
        return ret_string.format(self.subject, self.bill_num, self.score,
                                 self.logistic, self.actual)


class NY_Score(Base):
    __tablename__ = 'ny_score'
    subject = Column(String, primary_key=True)
    bill_num = Column(String, primary_key=True)
    score = Column(Float)
    logistic = Column(Float)

    def __repr__(self):
        ret_string = ("<NY_Score(subject={0}, bill_num={1}, score={2}, "
                      "logistic={3})>")
        return ret_string.format(self.subject, self.bill_num, self.score,
                                 self.logistic)


# Setup the database
def make_database():

    with open("./configs.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    dbname = cfg['dbname']
    username = cfg['username']

    engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

    # create a database (if it doesn't exist)
    if not database_exists(engine.url):
        create_database(engine.url)

    # Actually create the table
    Base.metadata.create_all(engine)
