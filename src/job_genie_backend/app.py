from __future__ import annotations

import hashlib
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db, init_db
from .models import User
from .schemas import UserSignup, UserRead

app = FastAPI(title="Job Genie Backend", version="0.1.0")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.post("/signup", response_model=UserRead, status_code=201)
def signup(user_in: UserSignup, db: Session = Depends(get_db)) -> User:
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
