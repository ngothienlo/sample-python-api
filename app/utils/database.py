from sqlalchemy import create_engine
from config.config import DATABASE_URL


def database_connection(db_url=DATABASE_URL):
    engine = create_engine(db_url)
    connection = engine.connect()
    return connection
