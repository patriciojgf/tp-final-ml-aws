"""Script to create DB tables."""
from database import models
from database import database as db

    
def create_tables_from_model():
    postgresclient=db.PostgresClient()
    models.Base.metadata.create_all(postgresclient._get_engine())