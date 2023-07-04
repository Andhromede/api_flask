from config import Base, engine
from sqlalchemy.orm import sessionmaker


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()