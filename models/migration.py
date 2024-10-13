from fastapi import HTTPException
from models.users_model import User
from models.items_model import Item
from services.database import engine, Base
    
def migration():
    try:

        print("Debug - Registered tables: ", Base.metadata.tables)

        if not Base.metadata.tables:
            print("No tables found for migration.")
        else:
            print("Tables to be migrated:", Base.metadata.tables.keys())
        
        Base.metadata.create_all(bind=engine)
        print("Database migrated successfully!")
        return {"message": "Database Connected"} 
    except HTTPException as e:
        raise e

class RunMigration:
    @staticmethod
    def run():
        migration()
