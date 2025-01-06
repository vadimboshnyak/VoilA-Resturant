import pytest
from utils.database import visitorsTable, gamesTable
from utils.utils import Queue, waitlistToDatabase, addtoWaitlist, displayAnalytics
from app import populateData

# Queue Test Enqueue
def test_Queue_enqueue():
    waitListQueue = Queue()

    waitListQueue.enqueue({"firstName": "Dillard",
    "lastName": "Flowers",
    "email": "dillard@gmail.com",
    "phoneNum": "0275243828",
    "date": "2025-01-03"})
    assert waitListQueue.size() == 1

    waitListQueue.enqueue({"firstName": "Test",
    "lastName": "TestLast",
    "email": "test@gmail.com",
    "phoneNum": "9999999999",
    "date": "2025-01-03"})
    assert waitListQueue.size() == 2

# Queue Test Remove
def test_Queue_remove():
    waitListQueue = Queue()

    waitListQueue.enqueue({"firstName": "Dillard",
    "lastName": "Flowers",
    "email": "dillard@gmail.com",
    "phoneNum": "0275243828",
    "date": "2025-01-03"})
    waitListQueue.enqueue({"firstName": "Test",
    "lastName": "TestLast",
    "email": "test@gmail.com",
    "phoneNum": "9999999999",
    "date": "2025-01-03"})
    assert waitListQueue.size() == 2

    popped = waitListQueue.remove()

    assert popped == {"firstName": "Dillard",
    "lastName": "Flowers",
    "email": "dillard@gmail.com",
    "phoneNum": "0275243828",
    "date": "2025-01-03"}
    assert waitListQueue.size() == 1

    popped = waitListQueue.remove()
    assert waitListQueue.size() == 0
    assert popped == {"firstName": "Test",
    "lastName": "TestLast",
    "email": "test@gmail.com",
    "phoneNum": "9999999999",
    "date": "2025-01-03"}

#To empty the database tables every test.
@pytest.fixture(autouse=True)
def databasesEmpty():
    visitorsTable.drop()
    gamesTable.drop()

"""
waitlist to database addition when we have the exact number of seats
attendance = 6998, seatsLeft = 2 
therefore we will get attendance=7000, seatsLeft=0, overflow=0, and waitlistQueue=0
"""
def test_waitlistToDatabaseExactSeats():
    gamesTable.insert_one({
        "date": "2025-01-03",
        "attendance": 6998,
        "overflow": 0
    })
    waitListQueue = Queue()

    waitListQueue.enqueue({"firstName": "Dillard",
    "lastName": "Flowers",
    "email": "dillard@gmail.com",
    "phoneNum": "0275243828",
    "date": "2025-01-03"})
    waitListQueue.enqueue({"firstName": "Test",
    "lastName": "TestLast",
    "email": "test@gmail.com",
    "phoneNum": "9999999999",
    "date": "2025-01-03"})

    waitlistToDatabase(waitListQueue, seatsLeft=2)

    assert waitListQueue.size() == 0
    
    game = gamesTable.find_one({"date": "2025-01-03"})

    assert game["attendance"] == 7000
    assert game["overflow"] == 0

"""
waitlist to database addition when we don't have enough seats
attendance = 6999, seatsLeft = 1
therefore we will get attendance=7000, seatsLeft=0, overflow=1, and waitlistQueue=1
"""
def test_waitlistToDatabaseOverFlow(capfd):
    gamesTable.insert_one({
        "date": "2025-01-03",
        "attendance": 6999,
        "overflow": 0
    })
    waitListQueue = Queue()

    waitListQueue.enqueue({"firstName": "Dillard",
    "lastName": "Flowers",
    "email": "dillard@gmail.com",
    "phoneNum": "0275243828",
    "date": "2025-01-03"})
    waitListQueue.enqueue({"firstName": "Test",
    "lastName": "TestLast",
    "email": "test@gmail.com",
    "phoneNum": "9999999999",
    "date": "2025-01-03"})

    waitlistToDatabase(waitListQueue, seatsLeft=1)

    out, error = capfd.readouterr()
 
    assert "The Restaurant have reached the limit capacity, unable to add more people from the waitlist. 1 were not allowed off the waitlist" in out
    assert waitListQueue.size() == 1
    
    game = gamesTable.find_one({"date": "2025-01-03"})

    assert game["attendance"] == 7000
    assert game["overflow"] == 1
"""
waitlist to database addition when we have more than enough seats
attendance = 6990, seatsLeft = 10 
therefore we will get attendance=6992, seatsLeft=8, overflow=0, and waitlistQueue=0
"""
def test_waitlistToDatabaseEnoughSeats():
    gamesTable.insert_one({
        "date": "2025-01-03",
        "attendance": 6990,
        "overflow": 0
    })
    waitListQueue = Queue()

    waitListQueue.enqueue({"firstName": "Dillard",
    "lastName": "Flowers",
    "email": "dillard@gmail.com",
    "phoneNum": "0275243828",
    "date": "2025-01-03"})
    waitListQueue.enqueue({"firstName": "Test",
    "lastName": "TestLast",
    "email": "test@gmail.com",
    "phoneNum": "9999999999",
    "date": "2025-01-03"})

    waitlistToDatabase(waitListQueue, seatsLeft=10)

    assert waitListQueue.size() == 0
    
    game = gamesTable.find_one({"date": "2025-01-03"})

    assert game["attendance"] == 6992
    assert game["overflow"] == 0

# Test to add guest to waitlist, tests input and addition to the queue.
def test_addtoWaitlist(monkeypatch):
    inputs = iter(["Vadim", "Boshnyak", "7056472222"])

    waitListQueue = Queue()
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    addtoWaitlist(waitListQueue, dateToBeAdded="2025-01-03")

    assert waitListQueue.size() == 1
    assert waitListQueue.peek()["firstName"] == "Vadim"
    assert waitListQueue.peek()["lastName"] == "Boshnyak"
    assert waitListQueue.peek()["phoneNum"] == "7056472222"

# Test to check for invalid input
def test_addtoWaitlistInvalidInput(monkeypatch, capfd):
    inputs = iter(["1231231231","Vadim", "Boshnyak", "7056472222"])

    waitListQueue = Queue()
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    addtoWaitlist(waitListQueue, dateToBeAdded="2025-01-03")

    out, error = capfd.readouterr()
    assert "Invalid Input" in out

# Test to check for adding a duplicate
def test_addtoWaitlistDuplicate(monkeypatch, capfd):
    inputs = iter(["Test", "TestLast", "9999999999"])

    waitListQueue = Queue()
    waitListQueue.enqueue({"firstName": "Test",
    "lastName": "TestLast",
    "email": "test@gmail.com",
    "phoneNum": "9999999999",
    "date": "2025-01-03"})
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    addtoWaitlist(waitListQueue, dateToBeAdded="2025-01-03")

    assert waitListQueue.size() == 1

    out, error = capfd.readouterr()
    assert "This person has already registered. Can not add this person." in out

    visitorsTable.insert_one({
        "firstName": "Vadim",
        "lastName": "Boshnyak",
        "phoneNum": "7056472222",
        "date": "2025-01-03"
    })

    inputs = iter(["Vadim", "Boshnyak", "7056472222"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    addtoWaitlist(waitListQueue, dateToBeAdded="2025-01-03")

    assert waitListQueue.size() == 1
    out, error = capfd.readouterr()
    assert "This person has already registered. Can not add this person." in out

# Test to populate data to the database and the queue using 2 small test JSONs
def test_populateData():
    # testWaitlist.json has 8 entries, testConfirmed.json has 5 entries.
    
    waitListQueue = Queue()
    populateData(waitListQueue, confirmedFile="testConfirmed.json", waitlistFile="testWaitlist.json")
    assert waitListQueue.size() == 8
    assert visitorsTable.count_documents({}) == 5

    game = gamesTable.find_one({"date" :"2025-01-03"})
    assert game["attendance"] == 5
    assert game

    assert waitListQueue.peek()["phoneNum"] == "0311924245"

    visitor = visitorsTable.find_one({"firstName" : "Charlene"})
    assert visitor
    assert visitor["phoneNum"] == "0938546205"

# Testing when we have an invalid file name
def test_populateDataInvalidFileName(capfd):
    # Testing for non existing files
    
    waitListQueue = Queue()
    populateData(waitListQueue, confirmedFile="blah.json", waitlistFile="test.json")
    out, error = capfd.readouterr()
    assert "Error: blah.json does not exist in the current directory." in out
    assert waitListQueue.size() == 0

    game = gamesTable.find_one({"date" :"2025-01-03"})
    assert game is None

    assert visitorsTable.count_documents({}) == 0

# Testing displaying analytics
def test_displayAnalytics(capfd, monkeypatch):
    dateInput = "2025-01-03"
    monkeypatch.setattr('builtins.input', lambda _: dateInput)
    waitListQueue = Queue()
    populateData(waitListQueue, confirmedFile="testConfirmed.json", waitlistFile="testWaitlist.json")

    displayAnalytics()
    out, error = capfd.readouterr()
    assert "Analytics for Date:  {0}".format(dateInput) in out

# Testing when we have no data for the given date
def test_displayAnalyticsInvalidDate(capfd, monkeypatch):
    dateInput = "2025-01-05"
    monkeypatch.setattr('builtins.input', lambda _: dateInput)

    waitListQueue = Queue()
    populateData(waitListQueue, confirmedFile="testConfirmed.json", waitlistFile="testWaitlist.json")

    displayAnalytics()
    out, error = capfd.readouterr()
    assert "Data for the date {0} is not available".format(dateInput) in out

# Testing invalid date format for analytics
def test_displayAnalyticsInvalidInput(capfd, monkeypatch):
    dateInput = iter(["05-01-2025", "2025-03-01"])
    monkeypatch.setattr('builtins.input', lambda _: next(dateInput))

    waitListQueue = Queue()
    populateData(waitListQueue, confirmedFile="testConfirmed.json", waitlistFile="testWaitlist.json")

    displayAnalytics()
    out, error = capfd.readouterr()
    assert "Invalid Date Format, Please Enter in ('YYYY-MM-DD') Format" in out

