import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, engine
import models  # registers all models

Base.metadata.create_all(bind=engine)