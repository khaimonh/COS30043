from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

db = SessionLocal()

for role_name in ("User", "Admin", "Staff"):
  existing_role = db.query(Role).filter(Role.role_name == role_name).first()
  if not existing_role:
      db.add(Role(role_name=role_name))