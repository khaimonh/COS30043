from sqlalchemy import select
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from api.database import SessionLocal
from api.models import Role


def seed_roles():
    db = SessionLocal()

    try:
        roles = ["Admin", "User"]

        for role_name in roles:
            existing_role = db.scalar(
                select(Role).where(Role.role_name == role_name)
            )

            if existing_role is None:
                db.add_all([Role(role_name="Admin"), Role(role_name="User")])

        db.commit()
        print("Roles seeded successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding roles: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()