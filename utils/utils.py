from utils.database import visitorsTable, gamesTable
from datetime import datetime

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)
    
    def remove(self):
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)
    
    def peek(self):
        return self.queue[0]
    
def waitlistToDatabase(waitListQueue, seatsLeft):
    if seatsLeft == 0:
        print("The Resturant have reached the limit capacity, unable to add more people from the waitlist. {0} were not allowed off the waitlist".format(waitListQueue.size()))
        return
    
    while waitListQueue.size() > 0:
        if seatsLeft == 0:
            print("The Resturant have reached the limit capacity, unable to add more people from the waitlist. {0} were not allowed off the waitlist".format(waitListQueue.size()))
            gamesTable.update_one(
            {"_id": currentGame["_id"]},
            {"$set": {"overflow": waitListQueue.size()}})
            return
        
        personToBeAdded = waitListQueue.remove()
        visitorsTable.insert_one(personToBeAdded)

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
    
    # Check if existing entry is visitors database
    existingInDB = visitorsTable.find_one({
        "firstName": firstName,
        "lastName": lastName,
        "phoneNum": phoneNum,
        "date": dateToBeAdded
    })

    # Check if it's in the waitlist queue
    existingInQueue = any(
        item["firstName"].lower() == firstName.lower() and
        item["lastName"].lower() == lastName.lower() and
        item["phoneNum"].lower() == phoneNum.lower() and
        item["date"].lower() == dateToBeAdded
        for item in waitListQueue.queue
    )
    if existingInDB or existingInQueue:
        print("This person has already registered. Can not add this person.")
        return
    waitListQueue.enqueue({"firstName": firstName, "lastName": lastName, "phoneNum": phoneNum, "date": dateToBeAdded})

def displayAnalytics():
    dateToCheck = ""
    while True:
        dateToCheck = input("Please Enter the date in the following format (YYYY-MM-DD): ")
        try:
            datetime.strptime(dateToCheck, "%Y-%m-%d")
            break
        except:
            print("Invalid Date Format, Please Enter in ('YYYY-MM-DD') Format")
    game = gamesTable.find_one({"date" : dateToCheck})

    if game is None:
        print("Data for the date {0} is not available".format(dateToCheck))
        return
    print("Analytics for Date: ", (game["date"]))
    print("Attendance: {0} People".format(game["attendance"]))
    print("Overflow (People that did not get off the waitlist): {0} People".format(game["overflow"]))