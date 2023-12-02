from pymongo import MongoClient

client = MongoClient("mongo", 27017, username="root", password="123456", serverSelectionTimeoutMS=5000)
db = client["db"]
User = db["users"]
User.create_index("username", unique=True)