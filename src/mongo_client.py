from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_NAME = "aws_arch"

client = MongoClient(os.getenv("MONGODB_URI"),
    # Set application name
    appname="moshe")

db = client[DATABASE_NAME]

def collection_exists(db, collection_name: str) -> bool:
    """
    Check if a MongoDB collection exists in the database.
    """
    return collection_name in db.list_collection_names()

def create_collection_if_not_exists(db, collection_name: str):
    """
    Create a MongoDB collection only if it does not already exist.
    """
    if not collection_exists(db, collection_name):
        db.create_collection(collection_name)
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")

create_collection_if_not_exists(db, "archi")