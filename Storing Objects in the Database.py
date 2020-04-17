from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class CheckingAccount(Base):
    x = 0

    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
        self.accountNumber = CheckingAccount.x + 1
        CheckingAccount.x = CheckingAccount.x + 1
        self.balance = 0

    __tablename__ = 'account'
    
    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    accountNumber = Column(Integer)
    balance = Column(Integer)
    
    def debit(self, debAmount):
        self.balance = self.balance - debAmount

    def credit(self, credAmount):
        self.balance = self.balance + credAmount
        
    def getBalance(self):
        print("The balance for account number", self.accountNumber, " is: ", self.balance)
    
def main():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    
    p1 = CheckingAccount("Sean", "Dunn")
    p2 = CheckingAccount("Pierre", "Dunn")
    
    p1.debit(100)
    p1.credit(350)
    p2.credit(100)
    p2.credit(400)
    p2.debit(155)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all([p1, p2])
    session.commit()

    for row in session.query(CheckingAccount).all():
        print (row.id, row.fname, row.lname, row.accountNumber, row.balance)
    
main()
