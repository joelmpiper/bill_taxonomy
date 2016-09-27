from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.ingest.setup_database import US_Score
from src.ingest.setup_database import NY_Score


def store_us_db(dbname, bills, subject, y_prob, y_true, cfg):

    if (subject.split(' ')[0] == 'Bank'):
        subject = subject.replace('capital', 'and capital')
    subject = subject.replace(' ', '_')
    subject = subject.replace(',', '')

    host = cfg['dbwrite_host']
    dbwrite_user = cfg['dbwrite_user']
    engine = create_engine('postgres://%s@%s/%s' % (dbwrite_user, host, dbname))

    # Open a session and connect to the database engine
    Session = sessionmaker(bind=engine)
    session = Session()
    for i, bill in enumerate(bills.iterrows()):

        # one_bill = US_Score(subject=subject, bill_num=bills['bill_num'][i],
        #                    actual=bool(y_true[i]), score=y_prob[i])
        # session.add(one_bill)
        score_column = cfg['score_column']
        bill_num = bills['bill_num'][i]
        session.query(US_Score).filter(US_Score.bill_num == bill_num,
                                       US_Score.subject == subject).update(
            {score_column: y_prob[i]})
    session.commit()
    session.close()
    return 0


def store_ny_db(dbname, bills, subject, y_prob, cfg):

    if (subject.split(' ')[0] == 'Bank'):
        subject = subject.replace('capital', 'and capital')
    subject = subject.replace(' ', '_')
    subject = subject.replace(',', '')

    host = cfg['dbwrite_host']
    dbwrite_user = cfg['dbwrite_user']
    engine = create_engine('postgres://%s@%s/%s' % (dbwrite_user, host, dbname))

    # Open a session and connect to the database engine
    Session = sessionmaker(bind=engine)
    session = Session()

    for i, bill in enumerate(bills.iterrows()):

        score_column = cfg['score_column']
        # one_bill = NY_Score(subject=subject, bill_num=bills['bill_num'][i],
        #                    score=y_prob[i])
        # session.add(one_bill)
        bill_num = bills['bill_num'][i]
        session.query(NY_Score).filter(NY_Score.bill_num == bill_num,
                                       NY_Score.subject == subject).update(
            {score_column: y_prob[i]})

    session.commit()
    session.close()
    return 0
