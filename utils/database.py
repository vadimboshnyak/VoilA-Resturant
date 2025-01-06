import pymongo

"""
Database setup, I have decided to have 2 tables for now as discussed on Friday during the interview. Visitors table holds all the people that were confirmed guests
with their information and a date of when they went. GameStats tracks the attendance of that night, and overflow (the people that did not get the chance to get off the waitlist)
I did this to track more analytics so the owner can see how many attended and how many people were overflowed to see what worked that night and what did not for the marketing
firstName, lastName, phoneNum and date are a compound index so we avoid duplicate registrations

Here I drop the tables in the beginning, once again this is just to show how the example works with the data, in the real app this would not be there as we need to track everything
"""

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
