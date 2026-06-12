from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.database import get_db
from app.models.models import User, Account, Transaction, TransactionType
from app.schemas.schemas import TransferRequest, TransactionOut, TransactionHistory
from app.core.security import get_current_user
from app.core.email import email_transfer_sender, email_transfer_receiver
import uuid
import threading

router = APIRouter()


def generate_reference() -> str:
    return f"TXN-{uuid.uuid4().hex[:12].upper()}"


@router.post("/transfer", response_model=TransactionOut)
def transfer(
    payload: TransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sender_account = db.query(Account).filter(Account.owner_id == current_user.id).first()
    if not sender_account:
        raise HTTPException(status_code=404, detail="Sender account not found")

    receiver_account = db.query(Account).filter(
        Account.account_number == payload.receiver_account_number
    ).first()
    if not receiver_account:
        raise HTTPException(status_code=404, detail="Receiver account not found")
    if sender_account.id == receiver_account.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to the same account")
    if sender_account.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    sender_account.balance -= payload.amount
    receiver_account.balance += payload.amount

    ref = generate_reference()
    txn = Transaction(
        reference=ref,
        transaction_type=TransactionType.transfer,
        amount=payload.amount,
        description=payload.description or f"Transfer to {receiver_account.account_number}",
        sender_account_id=sender_account.id,
        receiver_account_id=receiver_account.id,
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)

    # Email sender
    threading.Thread(
        target=email_transfer_sender,
        args=(current_user.full_name, current_user.email, payload.amount, receiver_account.account_number, sender_account.balance, ref),
        daemon=True,
    ).start()

    # Email receiver
    receiver_user = db.query(User).filter(User.id == receiver_account.owner_id).first()
    if receiver_user:
        threading.Thread(
            target=email_transfer_receiver,
            args=(receiver_user.full_name, receiver_user.email, payload.amount, sender_account.account_number, receiver_account.balance, ref),
            daemon=True,
        ).start()

    return txn


@router.get("/history/{account_number}", response_model=TransactionHistory)
def transaction_history(
    account_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    account = db.query(Account).filter(
        Account.account_number == account_number,
        Account.owner_id == current_user.id,
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    transactions = db.query(Transaction).filter(
        or_(
            Transaction.sender_account_id == account.id,
            Transaction.receiver_account_id == account.id,
        )
    ).order_by(Transaction.created_at.desc()).all()

    return {
        "account_number": account_number,
        "total_transactions": len(transactions),
        "transactions": transactions,
    }
