from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os

load_dotenv()

# Database configuration
db_url = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

class DatabaseService:
    """
    Database service for interacting with the PostgreSQL database.
    """
    def __init__(self):
        # Create the SQLAlchemy engine with connection pooling
        self.engine = create_engine(
            db_url,
            pool_size=10,  # Maximum connections in the pool
            max_overflow=5,  # Additional connections allowed above pool_size
            pool_timeout=30,  # Wait timeout for connections
            pool_pre_ping=True  # Ensures connections are alive
        )
        # Scoped session factory
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def get_session(self):
        """
        Get a new database session.
        """
        return self.Session()

    def close_session(self):
        """
        Remove the current session from the scoped session registry.
        """
        self.Session.remove()

    def dispose_engine(self):
        """
        Dispose of the engine and all connections in the pool.
        """
        self.engine.dispose()
