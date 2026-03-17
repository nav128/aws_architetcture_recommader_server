from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_NAME = "aws_arch"
COLLECTION_NAME = "services_profile"

client = MongoClient(os.getenv("MONGODB_URI"),
    # Set application name
    appname="moshe")



def ensure_database(uri="mongodb://user:pass@localhost:27017/", db_name="aws_arch"):
    """
    Ensures that the MongoDB database exists.
    Returns a reference to the database object.
    """
    
    # If the database already exists, this just returns it
    db = client[db_name]
    
    # Create a dummy collection if db is empty
    if db_name not in client.list_database_names():
        db["__init__"].insert_one({"init": True})
        db["__init__"].drop()  # remove dummy collection

    return db

# Example usage
db = ensure_database()


def create_collection_if_not_exists():
    """
    Create a MongoDB collection only if it does not already exist.
    """
    if not COLLECTION_NAME in db.list_collection_names():
        db.create_collection(COLLECTION_NAME)
        db[COLLECTION_NAME].create_index(
            [("vector", "vector")],   # 'vector' is the type of index
            vectorOptions={
                "dimensions": 50,     # must match the length of your one-hot vectors
                "metric": "cosine"    # "cosine", "euclidean", or "dotProduct"
            },
            name="vector_cosine"
        )
        print(f"Collection '{COLLECTION_NAME}' created.")
        


def ensure_collection() -> bool:
    """
    Check if a MongoDB collection exists in the database.
    """
    create_collection_if_not_exists()
    return  db[COLLECTION_NAME]
    
collection = ensure_collection()
