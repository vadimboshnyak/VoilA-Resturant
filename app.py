import os
import json
from datetime import date, datetime
from utils.database import visitorsTable, gamesTable
from utils.utils import Queue, addtoWaitlist, waitlistToDatabase, displayAnalytics

"""
Function to populate data from given JSONs files with a list of people. The files are in the following format [{"firstName": "Hobbs","lastName": "Crawford",
"phoneNum": "0844851659","date": "2025-01-03"}]. My logic here was that we will have an easy way to register a big file of people as it was described in the problem
with initial 2000 confirmed guests and 4000 waitlisted guests. It opens up the file using os, inserts data into the visitors table, then inserts an entity of a game 
to gamesTable. Then for each entry from the waitlisted json it adds to the waitlist queue.
"""
def populateData(waitListQueue, confirmedFile, waitlistFile):
    fileName = confirmedFile
    currentDir = os.path.dirname(os.path.abspath(__file__))
    dataDir = os.path.join(currentDir, "data")
    filePath = os.path.join(dataDir, fileName)

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

"""
Main function to run the app. Calls populateData to fill up the database tables from the JSON files in data folder. I have done because as the problem was explained as
the owner had two files, 1 waitlist file and 1 confirmed guests file. The date currently is hard coded for this example to show how the app and logic works.
I have made a simple menu that runs until the user inputs 4, every iteration, the statistics for the current date will be shown just so we see how many people in waitlist
how many people confirmed and how many seats left. If user selects 1, waitlist registration happens with input (addToWaitlist), if 2 then waitlisted people are added to 
the confirmed guests (waitlistToDatabase), if 3, display analytics will show (displayAnalytics)
"""
def main():

    waitListQueue = Queue()

 #   dateToday = date.today()
 #   dateToday = dateToday.strftime("%Y-%m-%d")
    dateToday = "2025-01-03"
    maxCapacity = 7000

    populateData(waitListQueue, confirmedFile = "confirmed.json", waitlistFile = "waitlist.json")
    print("\nWELCOME TO VoilA_Restaurant, The date is: {0}, Our Max Capacity is: {1} people".format(dateToday, maxCapacity))
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
        elif choice == "2" and waitListQueue.size() == 0:
            print("The waitlist is empty, add more visitors to the waitlist")
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