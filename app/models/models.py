from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class TransactionType(str, enum.Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"


class TransactionStatus(str, enum.Enum):
    success = "success"
    failed = "failed"
    pending = "pending"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    accounts = relationship("Account", back_populates="owner")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    account_name = Column(String, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    currency = Column(String, default="NGN")
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="accounts")
    sent_transactions = relationship("Transaction", foreign_keys="Transaction.sender_account_id", back_populates="sender_account")
    received_transactions = relationship("Transaction", foreign_keys="Transaction.receiver_account_id", back_populates="receiver_account")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, index=True, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.success)
    sender_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    receiver_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sender_account = relationship("Account", foreign_keys=[sender_account_id], back_populates="sent_transactions")
    receiver_account = relationship("Account", foreign_keys=[receiver_account_id], back_populates="received_transactions")
