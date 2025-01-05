import os
import json
from datetime import date, datetime
from utils.database import visitorsTable, gamesTable
from utils.utils import Queue, addtoWaitlist, waitlistToDatabase, displayAnalytics


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