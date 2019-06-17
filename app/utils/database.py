from sqlalchemy import create_engine
from ..app.config import DATABASE_URL


def database_connection(db_url=DATABASE_URL):
    connection = create_engine(db_url)
    return connection
