from pymongo import MongoClient

MONGO_URI = "mongodb+srv://jacobasuquo199:4e55kZKS4Dzwz7fJ@cluster0.e2rno.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)

try:
    # Check connection
    db_list = client.list_database_names()
    print(f"Connected to MongoDB. Databases: {db_list}")
except Exception as e:
    print(f"Error: {e}")



