import pymongo
import os
import json
from datetime import date

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

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)
    
    def remove(self):
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)
    
def waitlistToDatabase(waitListQueue, seatsLeft):

    while waitListQueue.size() > 0:
        if seatsLeft == 0:
            print("The Resturant have reached the limit capacity, unable to add more people from the waitlist. {0} were not allowed off the waitlist".format(waitListQueue.size()))
            gamesTable.update_one(
            {"_id": currentGame["_id"]},
            {"$set": {"overflow": waitListQueue.size()}})
            return
        
        personToBeAdded = waitListQueue.remove()
        gamesTable.insert_one(personToBeAdded)
        currentGame = gamesTable.find_one({"date": personToBeAdded["date"]})
        updatedAttendence = currentGame["attendance"] + 1
        gamesTable.update_one(
            {"_id": currentGame["_id"]},
            {"$set": {"attendance": updatedAttendence}})
        seatsLeft -= 1
    


def addtoWaitlist(waitListQueue, dateToBeAdded):
    while True:
        firstName = input("Enter your First Name: ")
        if firstName == "" or any(c.isdigit() for c in firstName):
            print("Invalid Input")
            continue
        break
    while True:
        lastName = input("Enter your Last Name: ")
        if lastName == "" or any(c.isdigit() for c in lastName):
            print("Invalid Input")
            continue
        break
    while True:
        phoneNum = input("Enter your Phone Number (6470009999 Format): ")
        if not phoneNum.isdigit() or len(phoneNum) != 10:
            print("Invalid Phone Number, make sure you only enter digits, and maximum 10 digits")
            continue
        break
    
    existingInDB = visitorsTable.find_one({
        "firstName": firstName,
        "lastName": lastName,
        "phoneNum": phoneNum,
        "date": dateToBeAdded
    })

    # Check if it's in the queue
    existingInQueue = any(
        item["firstName"] == firstName and
        item["lastName"] == lastName and
        item["phoneNum"] == phoneNum and
        item["date"] == dateToBeAdded
        for item in waitListQueue.queue
    )
    if existingInDB or existingInQueue:
        print("This person has already registered. Can not add this person.")
        return
    waitListQueue.enqueue({"firstName": firstName, "lastName": lastName, "phoneNum": phoneNum, "date": dateToBeAdded})


def initData(waitListQueue, confirmedFile = "confirmed.json", waitlistFile = "waitlist.json"):
    fileName = confirmedFile
    currentDir = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(currentDir, fileName)

    if not os.path.exists(filePath):
        print(f"Error: {fileName} does not exist in the current directory.")
        return
    
    with open(fileName, "r") as file:
        data = json.load(file)
    if visitorsTable.count_documents({"date": data[0]['date']}) > 0:
        return
    visitorsTable.insert_many(data)
    
    newGame = {"date": data[0]['date'], "attendance": len(data), "overflow": 0}
    gamesTable.insert_one(newGame)
    
    # Now populating to waitlist queue
    fileName = waitlistFile
    if not os.path.exists(filePath):
        print(f"Error: {fileName} does not exist in the current directory.")
        return
    with open(fileName, "r") as file:
        data = json.load(file)
    for entry in data:
        waitListQueue.enqueue(entry)


def main():

    waitListQueue = Queue()

 #   dateToday = date.today()
 #   dateToday = dateToday.strftime("%Y-%m-%d")
    dateToday = "2025-01-03"
    maxCapacity = 5000

    initData(waitListQueue)
    print("\nWELCOME TO VoilA_Restaurant, Today's date is: {0}, Our Max Capacity is: {1} people".format(dateToday, maxCapacity))
    print("================================================================\n\n")

    choice = "0"
    while choice != "3":
        currentCount = gamesTable.find_one({"date": dateToday})["attendance"]

        print("There are currently {0} Confirmed Guests".format(currentCount))
        print("There are currently {0} in the Waitlist".format(waitListQueue.size()))
        print("There are currently {0} Seats Left at the Restaurant".format(maxCapacity - currentCount))
        print("\n\nPlease choose an Option from below:")
        print("1. Add a New Visitor to the Waitlist")
        print("2. Add Waitlisted People to Confirmed Guests")
        print("3. Exit")
        choice = input("\nPlease Make a Selection: ")

        if choice == "1":
            addtoWaitlist(waitListQueue, dateToday)
        elif choice == "2":
            seatsLeft = maxCapacity - currentCount
            waitlistToDatabase(waitListQueue, seatsLeft)
        elif choice == "3":
            quit()


if __name__ == "__main__":
    main()