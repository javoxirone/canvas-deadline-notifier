from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

engine = create_engine("sqlite:///database.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()
