from os import path
import sys

package_path = path.abspath(path.join(path.dirname(__file__), '..'))
sys.path.insert(0, package_path)

# NOTE - You must import all models here that you want table generations for.
from models.Athlete import Base, Athlete
from models.Activity import Activity
from DatabaseService import DatabaseService

# Create the database service
db_service = DatabaseService()
engine = db_service.engine

# Create the tables
try:
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
except Exception as e:
    print(f"Error creating a table: {e}")
    raise
