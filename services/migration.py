from fastapi import HTTPException
from services.database import engine, Base
    
def migration():
    try:

        if not Base.metadata.tables:
            print("No tables found for migration.")
        else:
            print("Tables to be migrated:", Base.metadata.tables.keys())
        
        Base.metadata.create_all(bind=engine)
        print("Database migrated successfully!")
        return {"message": "Database Connected"} 
    except HTTPException as e:
        raise e

class Migration:
    @staticmethod
    def run():
        migration()
