from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from database.models import Base

engine = create_engine('sqlite:///app.db', connect_args={'check_same_thread': False})
db_session = scoped_session(sessionmaker(bind=engine))

def init_db():
    Base.metadata.create_all(bind=engine)
