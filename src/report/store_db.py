from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.ingest.setup_database import US_Score
from src.ingest.setup_database import NY_Score


def store_us_db(dbname, username, bills, subject, y_prob, y_true, cfg):

    engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

    # Open a session and connect to the database engine
    Session = sessionmaker(bind=engine)
    session = Session()

    for i, bill in enumerate(bills):

        one_bill = US_Score(subject=subject, bill_num=bills['bill_num'][i],
                            actual=bool(y_true[i]), score=y_prob[i])
        session.add(one_bill)
    session.commit()
    session.close()
    return 0


def store_ny_db(dbname, username, bills, subject, y_prob, cfg):
    engine = create_engine('postgres://%s@localhost/%s' % (username, dbname))

    # Open a session and connect to the database engine
    Session = sessionmaker(bind=engine)
    session = Session()

    for i, bill in enumerate(bills):

        one_bill = NY_Score(subject=subject, bill_num=bills['bill_num'][i],
                            score=y_prob[i])
        session.add(one_bill)

    session.commit()
    session.close()
    return 0
