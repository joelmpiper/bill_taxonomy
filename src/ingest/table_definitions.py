from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class NewYorkBills(Base):
    __tablename__ = 'ny_bills'
    bill_num = Column(String(20), primary_key=True)
    bill_name = Column(String(100))
    bill_text = Column(String)

    def __repr__(self):
        return f"<NewYorkBills(bill_num='{self.bill_num}', bill_name='{self.bill_name}', bill_text='{self.bill_text[:30]}...')>"

class UsBills(Base):
    __tablename__ = 'us_bills'
    bill_num = Column(String(20), primary_key=True)
    bill_name = Column(String(100))
    bill_text = Column(String)
    top_subject = Column(String(50))

    def __repr__(self):
        return f"<UsBills(bill_num='{self.bill_num}', bill_name='{self.bill_name}', bill_text='{self.bill_text[:30]}...', top_subject='{self.top_subject}')>"

class BillSubjects(Base):
    __tablename__ = 'bill_subjects'
    bill_num = Column(String(20), primary_key=True)
    subject = Column(String(50), primary_key=True)

    def __repr__(self):
        return f"<BillSubjects(bill_num='{self.bill_num}', subject='{self.subject}')>"

# Example usage
if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    new_bill = UsBills(bill_num="123", bill_name="Healthcare Reform", bill_text="An act to reform healthcare...", top_subject="Healthcare")
    session.add(new_bill)
    session.commit()

    retrieved_bill = session.query(UsBills).first()
    print(retrieved_bill)