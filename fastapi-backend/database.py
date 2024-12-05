from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from bcrypt import hashpw, gensalt, checkpw

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

def create_user(user):
    hashed_password = hashpw(user.password.encode(), gensalt())
    with SessionLocal() as session:
        session.add(User(username=user.username, email=user.email, password=hashed_password))
        session.commit()

def authenticate_user(email, password):
    with SessionLocal() as session:
        user = session.query(User).filter(User.email == email).first()
        if user and checkpw(password.encode(), user.password):
            return True
    return False

def get_users():
    with SessionLocal() as session:
        return session.query(User).all()
