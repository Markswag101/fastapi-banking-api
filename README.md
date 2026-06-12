# 🏦 FastAPI Banking REST API

A secure, production-ready banking REST API built with **FastAPI**, **SQLAlchemy**, and **JWT Authentication**.

Built by [Mark Ogunyemi](https://markswag101.github.io/Portfolio) — Senior Technical Programme Manager & Fintech Practitioner.

---

## 🚀 Features

- ✅ **User Registration & Login** with JWT authentication
- ✅ **Account Management** — create and view bank accounts
- ✅ **Deposits & Withdrawals** with transaction records
- ✅ **Fund Transfers** between accounts with balance validation
- ✅ **Transaction History** per account
- ✅ **Auto-generated** 10-digit account numbers & transaction references
- ✅ **Interactive API Docs** via Swagger UI

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Auth | JWT (python-jose) |
| Validation | Pydantic v2 |
| Password Hashing | bcrypt (passlib) |

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Markswag101/fastapi-banking-api.git
cd fastapi-banking-api
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
uvicorn app.main:app --reload
```

### 5. Open API docs
```
http://localhost:8000/docs
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Login and receive JWT token |
| GET | `/api/v1/auth/me` | Get current user profile |

### Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/accounts/` | Create a new account |
| GET | `/api/v1/accounts/` | List all accounts |
| GET | `/api/v1/accounts/{account_number}` | Get account details |
| POST | `/api/v1/accounts/{account_number}/deposit` | Deposit funds |
| POST | `/api/v1/accounts/{account_number}/withdraw` | Withdraw funds |

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/transactions/transfer` | Transfer funds between accounts |
| GET | `/api/v1/transactions/history/{account_number}` | Get transaction history |

---

## 🔐 Authentication Flow

1. Register at `POST /api/v1/auth/register`
2. Login at `POST /api/v1/auth/login` → receive `access_token`
3. Pass token in header: `Authorization: Bearer <token>`

---

## 📁 Project Structure

```
fastapi-banking-api/
├── app/
│   ├── main.py              # App entry point
│   ├── core/
│   │   └── security.py      # JWT & password hashing
│   ├── db/
│   │   └── database.py      # SQLAlchemy setup
│   ├── models/
│   │   └── models.py        # DB models (User, Account, Transaction)
│   ├── routers/
│   │   ├── auth.py          # Auth endpoints
│   │   ├── accounts.py      # Account endpoints
│   │   └── transactions.py  # Transfer & history endpoints
│   └── schemas/
│       └── schemas.py       # Pydantic request/response schemas
├── requirements.txt
└── README.md
```

---

## 🌍 Deployment

To deploy on **Railway**, **Render**, or **Heroku**, replace the SQLite URL in `app/db/database.py` with your PostgreSQL connection string:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host/dbname"
```

---

## 📄 License

MIT License — free to use and adapt.
