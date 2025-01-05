import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["VoilA_Restaurant"]

visitorsTable = db["Visitors"]
gamesTable = db["GameStats"]
visitorsTable.drop()
gamesTable.drop()
visitorsTable.create_index(
    [
        ("firstName", 1),
        ("lastName", 1),
        ("phoneNum", 1),
        ("date", 1)
    ],
    unique=True
)
