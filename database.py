import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["VoilA_Restaurant"]

visitorsTable = db["Visitors"]
visitorsTable.create_index(
    [
        ("firstName", 1),
        ("lastName", 1),
        ("phone", 1),
        ("date", 1)
    ],
    unique=True
)

gamesTable = db["GameStats"]
visitorsTable.drop()
gamesTable.drop()