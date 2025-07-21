from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, auth, db

router = APIRouter()

@router.post("/register")
def register(user: schemas.UserCreate, session: Session = Depends(db.get_db)):
    db_user = session.query(models.User).filter_by(email=user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = auth.hash_password(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw)
    session.add(new_user)
    session.commit()
    return {"msg": "User created"}

@router.post("/login")
def login(user: schemas.UserLogin, session: Session = Depends(db.get_db)):
    db_user = session.query(models.User).filter_by(email=user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
