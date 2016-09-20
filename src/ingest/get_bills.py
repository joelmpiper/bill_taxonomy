import psycopg2
import pandas as pd


def get_us_bills(dbname, username, us_subset):
    """ Retrieve the subset of bills from the U.S. Congress for 114th term
    """

    con = psycopg2.connect(database=dbname, user=username)
    # query:
    sql_str = """
    SELECT bill_num, bill_name, bill_text FROM us_bills
    LIMIT {0}
    """
    sql_query = sql_str.format(us_subset)
    us_bills = pd.read_sql_query(sql_query, con)
    return us_bills


def get_ny_bills(dbname, username, ny_subset):
    """ Retrieve the subset of bills from the NY legislature for 2015
    """

    con = psycopg2.connect(database=dbname, user=username)
    # query:
    sql_str = """
    SELECT bill_num, bill_name, bill_text FROM ny_bills
    LIMIT {0}
    """
    sql_query = sql_str.format(ny_subset)
    ny_bills = pd.read_sql_query(sql_query, con)
    return ny_bills


def get_subjects(dbname, username, subjects):
    """ Retrieve the subset of subjects associated with bills from
        U.S. Congress for 114th term
    """

    con = psycopg2.connect(database=dbname, user=username)
    # query:
    sql_str = """
    SELECT bill_num, subject FROM bill_subject
    WHERE subject IN ('{0}')
    """
    sql_query = sql_str.format("','".join(subjects))
    subjects = pd.read_sql_query(sql_query, con)
    return subjects
