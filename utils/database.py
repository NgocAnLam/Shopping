from pymongo import MongoClient

def connectDB():
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    return client['NgocDungStore']

if __name__ == "__main__":   
    dbname = connectDB()