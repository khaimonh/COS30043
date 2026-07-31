import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from api.database import Base, engine
from api import models
from utils.database.seed_roles import seed_roles


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

seed_roles()