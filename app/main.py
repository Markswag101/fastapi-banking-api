from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routers import auth, accounts, transactions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Banking API",
    description="A secure banking REST API with JWT authentication, account management, transfers, and transaction history.",
    version="1.0.0",
    contact={
        "name": "Mark Ogunyemi",
        "url": "https://markswag101.github.io/Portfolio",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])


@app.get("/", tags=["Health"])
def root():
    return {"message": "FastAPI Banking API is running", "version": "1.0.0", "docs": "/docs"}
