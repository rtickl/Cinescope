from sqlalchemy import Column, String, Integer

from db_models.movies import Base


class AccountTransactionTemplate(Base):
    __tablename__ = 'accounts_transaction_template'
    user = Column(String, primary_key=True)
    balance = Column(Integer, nullable=False)
    