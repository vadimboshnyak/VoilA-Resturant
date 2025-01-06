from utils.database import visitorsTable, gamesTable
from datetime import datetime

# Basic Queue implementation from a python array instead of using collections.
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

"""
Inputs: waitlistQueue (our queue that holds the waitlist), seatsLeft (int with how many seats left in the restaurant) returns nothing
Implementation: loop until waitlistQueue is empty, if seatsLeft is 0, I output that capacity has reached and update the gamesTable with the overflow 
(the size of the waitlist queue) because that is how many people did not get off the waitlist. I pop from queue, add that person to the confirmed database and increment
the gamesTable current game attendance buy 1, and decrement seatsLeft by 1. The whole point of this is to remove the people coming off the waitlist and add them to 
the visitors table.
"""    
def waitlistToDatabase(waitListQueue, seatsLeft):
    
    while waitListQueue.size() > 0:
        if seatsLeft == 0:
            print("The Restaurant have reached the limit capacity, unable to add more people from the waitlist. {0} were not allowed off the waitlist".format(waitListQueue.size()))
            gamesTable.update_one(
            {"_id": currentGame["_id"]},
            {"$set": {"overflow": waitListQueue.size()}})
            return
        
        personToBeAdded = waitListQueue.remove()
        visitorsTable.insert_one(personToBeAdded)

        currentGame = gamesTable.find_one({"date": personToBeAdded["date"]})
        updatedAttendance = currentGame["attendance"] + 1
        gamesTable.update_one(
            {"_id": currentGame["_id"]},
            {"$set": {"attendance": updatedAttendance}})
        seatsLeft -= 1
    

"""
Inputs: waitlistQueue (our queue that holds the waitlist), dateToBeAdded (string date) returns nothing
Implementation: get input from the user (first last, last name and phone number), validate it, check if entry is either in the database or in the waitlist queue,
if yes deny the entry as we do not want duplicate entries. If not, then add to the waitlist queue. This is the registration part of the user to the waitlist. Currently
it only allows the current date or the date passed in, but in the working app the person should select the date to enter the waitlist, for example a datepicker from React
would be a great component to use here.
"""    
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


"""
Inputs: None returns None
Implementation: To display analytics of a certain date. Asks for date input and validates it, then searches the gamesTable to find if there was an event on this date
outputs the date, attendance for that day and the overflow. I did this so the owner can see each day and how well the night went to think about the marketing strategy
"""    
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