import psycopg2
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import bills.wrangle.create_corpus
from bills.ingest.setup_database import Subject_Score
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sklearn.linear_model import LogisticRegression
import pickle
import yaml


class Bill_Info(object):
    """ class to store bill information """

    def __init__(self):
        with open("../configs.yml", 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile)


def get_bill_info(dbname, username, subject):
    con = psycopg2.connect(database=dbname, user=username)

    # query:
    sql_query = """
    SELECT bill_num, bill_name, bill_text FROM us_bills
    """
    us_bills = pd.read_sql_query(sql_query, con)

    sql_query = """
    SELECT bill_num, subject FROM bill_subject
    WHERE subject='{0}'
    """

    subject_terms = pd.read_sql_query(sql_query.format(subject), con)
    subject_col_name = subject.lower().replace(' ', '_')

    us_bills[subject_col_name] = 0
    us_bills.ix[us_bills['bill_num'].isin(subject_terms['bill_num']),
                subject_col_name] = 1
    # X = us_bills[['bill_name', 'bill_text']]
    X = us_bills['bill_text']
    y = us_bills[subject_col_name]
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    return X_train, X_test, y_train, y_test


def get_us_data(dbname, username, subject, model, model_type='naive_bayes'):

    X_train, X_test, y_train, y_test = get_bill_info(dbname, username,
                                                     subject)

    X_train_dtm = model.fit_transform(X_train)
    X_test_dtm = model.transform(X_test)

    # use Naive Bayes to predict the star rating
    mod = MultinomialNB()
    if(model_type == 'naive_bayes'):
        mod = MultinomialNB()

    elif(model_type == 'logistic'):
        mod = LogisticRegression(C=1e9, penalty='l1')
    mod.fit(X_train_dtm, y_train)
    y_pred_class = mod.predict(X_test_dtm)

    y_pred_prob = mod.predict_proba(X_test_dtm)[:, 1]

    combo_results = [mod, model, y_pred_class, y_pred_prob,
                     X_train_dtm, X_test_dtm, y_train,
                     y_test]
    pickle.dump(combo_results,
                open(('/Users/Joel/Desktop/Insight/data/model.p'), 'wb'))

    # return (metrics.accuracy_score(y_test, y_pred_class),
    #        metrics.confusion_matrix(y_test, y_pred_class),
    #        len(y_pred_prob))

    print(metrics.accuracy_score(y_test, y_pred_class))
    print(metrics.confusion_matrix(y_test, y_pred_class))
    print(max(y_pred_prob))

    return model, mod


# create a score for all of the subjects
def score_all_subjects():

    with open("configs.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    dbname = cfg['dbname']
    username = cfg['username']
    model_type = cfg['model_type']
    subset_size = cfg['subset_size']
    score_pickle_dest = cfg['output_dir']

    subjects = ['Competition and antitrust', 'Bank accounts, deposits, capital',
                'Bankruptcy', 'Employee benefits and pensions',
                'Intellectual property', 'Labor and employment', 'Securities',
                'Taxation']

    pairs = []
    for sub in subjects:
        pairs.append(score_ny_bills(dbname, username, sub, model_type,
                                    subset_size))

    pickle.dump(pairs,
                open((score_pickle_dest), 'wb'))


def score_ny_bills(dbname='bills_db', username='Joel', subject="Health",
                   model_type="naive_bayes", subset_size=None):

    con = psycopg2.connect(database=dbname, user=username)
    # query:
    sql_query = """
    SELECT bill_num, bill_name, bill_text FROM ny_bills
    """
    ny_bills = pd.read_sql_query(sql_query, con)

    # include 1-grams and 2-grams, we end up with many features
    vect = CountVectorizer(stop_words='english')

    transformer, trained_model = get_us_data(dbname, username, subject, vect,
                                             model_type)
    X_ny = transformer.transform(ny_bills['bill_text'])
    probs = trained_model.predict_proba(X_ny)[:, 1]

    pairs = [(ny_bills.ix[i, 'bill_name'],
              probs[i]) for i in range(0, len(ny_bills))]

    # store_results(dbname, username, subject, ny_bills['bill_num'], probs)

    return pairs


def store_results(dbname, username, subject, bill_nums, probs):

    engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

    # Open a session and connect to the database engine
    Session = sessionmaker(bind=engine)
    session = Session()

    for i, bill in enumerate(bill_nums):

        one_bill = Subject_Score(subject=subject, bill_num=bill,
                                 score=probs[i])
        session.add(one_bill)
    session.commit()
    session.close()


def create_lda_tfidf(dbname='bills_db', username='Joel'):

    X_train, X_test, y_train, y_test = get_bill_info(dbname, username)

    # create corpus, lda, tf/idf model using the training data
    title_corpus, text_corpus = bills.wrangle.create_corpus.real_corpus(
        X_train['bill_name'], X_train['bill_text'])

    # apply the lda model on the X_train

    # apply the tf/idf model on the X_train
    return bills.wrangle.create_corpus.create_corpora(X_train['bill_name'],
                                                      X_train['bill_text'])
    # combine these two as input vectors

    # run the logistic regression on those sets of features
