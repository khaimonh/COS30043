import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from api.database import Base, engine
from api import models


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)