from sqlalchemy import select
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from api.database import SessionLocal
from api.models import Role


def seed_roles():
      db = SessionLocal()
      try:
          for role_name in ["Admin", "User"]:
              if db.scalar(select(Role).where(Role.role_name == role_name)) is None:
                  db.add(Role(role_name=role_name))
          db.commit()
      except Exception:
          db.rollback()
          raise
      finally:
          db.close()


if __name__ == "__main__":
    seed_roles()