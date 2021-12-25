from Yuriko import MONGO_DB_URI
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_DB_URI") 

mongoPY = MongoClient(MONGO_URI)
