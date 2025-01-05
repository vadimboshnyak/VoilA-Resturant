import os
import json
from datetime import date, datetime
from database import visitorsTable, gamesTable

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


def populateData(waitListQueue, confirmedFile, waitlistFile):
    fileName = confirmedFile
    currentDir = os.path.dirname(os.path.abspath(__file__))
    dataDir = os.path.join(currentDir, "data")
    filePath = os.path.join(dataDir, fileName)
    print(filePath)

    if not os.path.exists(filePath):
        print(f"Error: {fileName} does not exist in the current directory.")
        return
    
    with open(filePath, "r") as file:
        data = json.load(file)
    if visitorsTable.count_documents({"date": data[0]['date']}) > 0:
        return
    visitorsTable.insert_many(data)
    
    newGame = {"date": data[0]['date'], "attendance": len(data), "overflow": 0}
    gamesTable.insert_one(newGame)
    
    # Now populating to waitlist queue
    fileName = waitlistFile
    filePath = os.path.join(dataDir, fileName)
    if not os.path.exists(filePath):
        print(f"Error: {fileName} does not exist in the current directory.")
        return
    with open(filePath, "r") as file:
        data = json.load(file)
    for entry in data:
        waitListQueue.enqueue(entry)

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


def main():

    waitListQueue = Queue()

 #   dateToday = date.today()
 #   dateToday = dateToday.strftime("%Y-%m-%d")
    dateToday = "2025-01-03"
    maxCapacity = 7000

    populateData(waitListQueue, confirmedFile = "confirmed.json", waitlistFile = "waitlist.json")
    print("\nWELCOME TO VoilA_Restaurant, Today's date is: {0}, Our Max Capacity is: {1} people".format(dateToday, maxCapacity))
    print("================================================================")

    choice = "0"
    dateToCheck = ""
    while choice != "4":
        currentCount = gamesTable.find_one({"date": dateToday})["attendance"]
        seatsLeft = maxCapacity - currentCount
        print("\nThere are currently {0} Confirmed Guests".format(currentCount))
        print("There are currently {0} in the Waitlist".format(waitListQueue.size()))
        print("There are currently {0} Seats Left at the Restaurant".format(maxCapacity - currentCount))
        print("\n\nPlease choose an Option from below:")
        print("1. Add a New Visitor to the Waitlist")
        print("2. Add Waitlisted People to Confirmed Guests")
        print("3. Display Analytics")
        print("4. Exit")
        choice = input("\nPlease Make a Selection: ")

        if choice == "1" and seatsLeft > 0:
            addtoWaitlist(waitListQueue, dateToday)
        elif choice == "2" and seatsLeft > 0:
            waitlistToDatabase(waitListQueue, seatsLeft)
        elif choice == "2" or choice == "1" and seatsLeft <= 0:
            print("We have reached capacity, we can not add new guests to the waitlist")
        elif choice == "3":
            displayAnalytics()
        elif choice == "4":
            quit()
        


if __name__ == "__main__":
    main()