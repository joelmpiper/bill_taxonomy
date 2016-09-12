import psycopg2
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer


def get_us_data(dbname='bills_db', username='Joel'):
    con = psycopg2.connect(database=dbname, user=username)

    # query:
    sql_query = """
    SELECT * FROM us_bills;
    """
    us_bills = pd.read_sql_query(sql_query, con)

    us_bills['marine_and_inland_water_transportation'] = 0

    # query:
    sql_query = """
    SELECT bill_num, subject FROM bill_subject
    WHERE subject='Marine and inland water transportation';
    """
    marine_terms = pd.read_sql_query(sql_query, con)

    us_bills.ix[us_bills['bill_num'].isin(marine_terms['bill_num']),
                'marine_and_inland_water_transportation'] = 1
    X = us_bills['bill_text']
    y = us_bills['marine_and_inland_water_transportation']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    # include 1-grams and 2-grams, we end up with many features
    vect = CountVectorizer(lowercase=False, ngram_range=(1, 2),
                           stop_words='english')
    X_train_dtm = vect.fit_transform(X_train)
    X_test_dtm = vect.transform(X_test)

    # use Naive Bayes to predict the star rating
    nb = MultinomialNB()
    nb.fit(X_train_dtm, y_train)
    y_pred_class = nb.predict(X_test_dtm)

    y_pred_prob = nb.predict_proba(X_test_dtm)[:, 1]

    return (metrics.accuracy_score(y_test, y_pred_class),
            metrics.confusion_matrix(y_test, y_pred_class),
            y_pred_prob[0:10])
