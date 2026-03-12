from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql://kavin:kingkavin000@localhost:5432/kavin"

engine =   create_engine(db_url)
session = sessionmaker(autocommit=False,autoflush=False,bind=engine)



