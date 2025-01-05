import pytest
from utils.database import visitorsTable, gamesTable
from utils.utils import Queue, waitlistToDatabase, addtoWaitlist, displayAnalytics
from app import populateData

# Queue Tests
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

@pytest.fixture(autouse=True)
def databasesEmpty():
    visitorsTable.drop()
    gamesTable.drop()


def test_waitlistToDatabaseExactSeats():
    gamesTable.insert_one({
        "date": "2025-01-03",
        "attendance": 0,
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

    assert game["attendance"] == 2
    assert game["overflow"] == 0

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

    assert "The Resturant have reached the limit capacity, unable to add more people from the waitlist. 1 were not allowed off the waitlist" in out
    assert waitListQueue.size() == 1
    
    game = gamesTable.find_one({"date": "2025-01-03"})

    assert game["attendance"] == 7000
    assert game["overflow"] == 1

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

    waitlistToDatabase(waitListQueue, seatsLeft=8)

    assert waitListQueue.size() == 0
    
    game = gamesTable.find_one({"date": "2025-01-03"})

    assert game["attendance"] == 6992
    assert game["overflow"] == 0

def test_addtoWaitlist(monkeypatch):
    inputs = iter(["Vadim", "Boshnyak", "7056472222"])

    waitListQueue = Queue()
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    addtoWaitlist(waitListQueue, dateToBeAdded="2025-01-03")

    assert waitListQueue.size() == 1
    assert waitListQueue.peek()["firstName"] == "Vadim"
    assert waitListQueue.peek()["lastName"] == "Boshnyak"
    assert waitListQueue.peek()["phoneNum"] == "7056472222"

def test_addtoWaitlistInvalidInput(monkeypatch, capfd):
    inputs = iter(["1231231231","Vadim", "Boshnyak", "7056472222"])

    waitListQueue = Queue()
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    addtoWaitlist(waitListQueue, dateToBeAdded="2025-01-03")

    out, error = capfd.readouterr()
    assert "Invalid Input" in out

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


def test_displayAnalytics(capfd, monkeypatch):
    dateInput = "2025-01-03"
    monkeypatch.setattr('builtins.input', lambda _: dateInput)
    waitListQueue = Queue()
    populateData(waitListQueue, confirmedFile="testConfirmed.json", waitlistFile="testWaitlist.json")

    displayAnalytics()
    out, error = capfd.readouterr()
    assert "Analytics for Date:  {0}".format(dateInput) in out

def test_displayAnalyticsInvalidDate(capfd, monkeypatch):
    dateInput = "2025-01-05"
    monkeypatch.setattr('builtins.input', lambda _: dateInput)

    waitListQueue = Queue()
    populateData(waitListQueue, confirmedFile="testConfirmed.json", waitlistFile="testWaitlist.json")

    displayAnalytics()
    out, error = capfd.readouterr()
    assert "Data for the date {0} is not available".format(dateInput) in out

def test_displayAnalyticsInvalidInput(capfd, monkeypatch):
    dateInput = iter(["05-01-2025", "2025-03-01"])
    monkeypatch.setattr('builtins.input', lambda _: next(dateInput))

    waitListQueue = Queue()
    populateData(waitListQueue, confirmedFile="testConfirmed.json", waitlistFile="testWaitlist.json")

    displayAnalytics()
    out, error = capfd.readouterr()
    assert "Invalid Date Format, Please Enter in ('YYYY-MM-DD') Format" in out

