import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["VoilA_Restaurant"]

visitors = db["Visitors"]
games = db["GameStats"]


# - 7000 PEOPLE
# - 2000 Ready to go
# - 4000 WAITLIST 
# - QUEUE Datastructure 
# - Database for the registered members
#     -TABLE1 : Names, Date of the game
#     -Table2: Date of the game, Attendance


#     Add the 2000 ready to go people to the database

#     This would be a prompt: for the waitlist, ask the person for personal information = names, date of the game

#     Use the waitlist as a queue, once a member is off pop off the queue and add it to database table1 and table2 for the attendence (+1)



class Person:
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

class Game:
    def __init__(self, date):
        self.date = date
        self.attendance = 0


# --MONGODB CREATE Visitors

# jsonObj = {
#     firstName = firstName
#     lastName = lastName
#     date = dateOfTheGame
# }

# --Mongodb create GameStats

# jsonObj = {
#     date = dateOfTheGame
#     attendance = int of visitors
# }

# arrPeople = [{firstName, lastName, game}]

# --MongoDB.insertMany(arrPeople)

# --MongoDB.GameStats.insert(date, len(arrPeople))


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)
    
    def remove(self):
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)
    
# def waitlistToDatabase():
#     arrWaitlist = []
#     pplCount = 0
#     for person in arrWaitlist:
#         queue.enqueue(person)


#     for person in queue:
#         personToBeAdded = queue.remove()

#         --MongoDb Vistiors.insert(personToBeAdded)

#         pplCount += 1
    
#     currentPplCount = --MongoDB GameStats.get(pplCount)
#     --MongoDB GameStats.update(date, pplCount+currentPplCount)






