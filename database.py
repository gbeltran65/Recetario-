from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://ukrd2ajoorjc2gectpkj:Uc7tY56R6IcP6s5pcPRJUMX3mXU8du@bjgwofsjrdjrveucsnel-postgresql.services.clever-cloud.com:50013/bjgwofsjrdjrveucsnel"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
