from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models.models import TransactionType, TransactionStatus


# ── Auth Schemas ──────────────────────────────────────────────
class UserCreate(BaseModel):
    full_name: str = Field(..., example="Mark Ogunyemi")
    email: EmailStr = Field(..., example="mark@example.com")
    phone: Optional[str] = Field(None, example="+2348012345678")
    password: str = Field(..., min_length=6, example="securepass123")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ── Account Schemas ───────────────────────────────────────────
class AccountCreate(BaseModel):
    currency: Optional[str] = Field("NGN", example="NGN")


class DepositWithdraw(BaseModel):
    amount: float = Field(..., gt=0, example=10000.00)
    description: Optional[str] = Field(None, example="Salary deposit")


class AccountOut(BaseModel):
    id: int
    account_number: str
    account_name: str
    balance: float
    currency: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Transaction Schemas ───────────────────────────────────────
class TransferRequest(BaseModel):
    receiver_account_number: str = Field(..., example="9876543210")
    amount: float = Field(..., gt=0, example=5000.00)
    description: Optional[str] = Field(None, example="Rent payment")


class TransactionOut(BaseModel):
    id: int
    reference: str
    transaction_type: TransactionType
    amount: float
    description: Optional[str]
    status: TransactionStatus
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionHistory(BaseModel):
    account_number: str
    total_transactions: int
    transactions: List[TransactionOut]
