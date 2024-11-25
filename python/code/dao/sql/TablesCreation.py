from os import path
import sys

package_path = path.abspath(path.join(path.dirname(__file__), '..'))
sys.path.insert(0, package_path)

from models.Activity import Base as BaseActivity
from models.Athlete import Base as BaseAthlete
from DatabaseService import DatabaseService

# Create the database service
db_service = DatabaseService()
engine = db_service.engine

# Create the 'athletes' table if it doesn't already exist
try:
    BaseAthlete.metadata.create_all(engine)
    print("'athletes' table created successfully!")
except Exception as e:
    print(f"Error creating the 'athletes' table: {e}")
    raise

# Create the 'activities' table if it doesn't already exist
try:
    BaseActivity.metadata.create_all(engine)
    print("'activities' table created successfully!")
except Exception as e:
    print(f"Error creating the 'activities' table: {e}")
    raise