from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

from sqlalchemy_utils import database_exists, create_database
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_database():
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
    if not database_exists(engine.url):  # Checks for the first time
        logger.info("Database "+settings.POSTGRES_DB +
                    " doesn't exist yet, let's try to create it")
        create_database(engine.url)     # Create new DB
        logger.info("Database Created")
        just_created = True
    else:
        logger.info("Database Already Exists")
        just_created = False
    return (engine, just_created)


engine, just_created = validate_database()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
