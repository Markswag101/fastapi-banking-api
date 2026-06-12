from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User, Account, Transaction, TransactionType
from app.schemas.schemas import AccountCreate, AccountOut, DepositWithdraw, TransactionOut
from app.core.security import get_current_user
from app.core.email import email_deposit, email_withdrawal
from typing import List
import random
import uuid
import threading

router = APIRouter()


def generate_account_number() -> str:
    return "".join([str(random.randint(0, 9)) for _ in range(10)])


def generate_reference() -> str:
    return f"TXN-{uuid.uuid4().hex[:12].upper()}"


@router.post("/", response_model=AccountOut, status_code=status.HTTP_201_CREATED)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    acc_number = generate_account_number()
    while db.query(Account).filter(Account.account_number == acc_number).first():
        acc_number = generate_account_number()

    account = Account(
        account_number=acc_number,
        account_name=current_user.full_name,
        balance=0.0,
        currency=payload.currency or "NGN",
        owner_id=current_user.id,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.get("/", response_model=List[AccountOut])
def list_accounts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Account).filter(Account.owner_id == current_user.id).all()


@router.get("/{account_number}", response_model=AccountOut)
def get_account(account_number: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = db.query(Account).filter(
        Account.account_number == account_number,
        Account.owner_id == current_user.id,
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.post("/{account_number}/deposit", response_model=TransactionOut)
def deposit(
    account_number: str,
    payload: DepositWithdraw,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = db.query(Account).filter(
        Account.account_number == account_number,
        Account.owner_id == current_user.id,
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account.balance += payload.amount
    ref = generate_reference()
    txn = Transaction(
        reference=ref,
        transaction_type=TransactionType.deposit,
        amount=payload.amount,
        description=payload.description or "Deposit",
        receiver_account_id=account.id,
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)

    # Send deposit email in background
    threading.Thread(
        target=email_deposit,
        args=(current_user.full_name, current_user.email, payload.amount, account_number, account.balance, ref),
        daemon=True,
    ).start()

    return txn


@router.post("/{account_number}/withdraw", response_model=TransactionOut)
def withdraw(
    account_number: str,
    payload: DepositWithdraw,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = db.query(Account).filter(
        Account.account_number == account_number,
        Account.owner_id == current_user.id,
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    account.balance -= payload.amount
    ref = generate_reference()
    txn = Transaction(
        reference=ref,
        transaction_type=TransactionType.withdrawal,
        amount=payload.amount,
        description=payload.description or "Withdrawal",
        sender_account_id=account.id,
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)

    # Send withdrawal email in background
    threading.Thread(
        target=email_withdrawal,
        args=(current_user.full_name, current_user.email, payload.amount, account_number, account.balance, ref),
        daemon=True,
    ).start()

    return txn
