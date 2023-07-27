from weather_api_caller.mongodb.MongoDataBase import MongoDataBase

db = MongoDataBase("application")
db.collection.drop()
