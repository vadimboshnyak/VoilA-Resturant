# VoilA-Resturant Management System

## My Implementation For The Interview Question

### Assumptions

1. If we have 7,000 confirmed guests, we can not add more people to the waiting list.
2. There are no cancellations, if someone signs up, they are going.
3. Date format follows YYYY-MM-DD format
4. Duplicate entries are not allowed, it is being filtered and checked by the combination of first name, last name and phone number. This is done by making a unique compound index.
5. 2 file inputs needed to run, waitList.json and confirmed.json, both are in the following JSON format:

   ```bash
   [
       {
        "firstName": "Hobbs",
        "lastName": "Crawford",
        "phoneNum": "0844851659",
        "date": "2025-01-03"
       }
   ]
   ```

   They should be placed in the data folder.

6. Currently the date is hard coded, but can easily be changed to today's date (the code is commented out). This is just to show a running example.

### Prerequisites

1. Python 3.x installed on your system.
2. MongoDB running locally or on a server. Currently configured like this: mongodb://localhost:27017/. Can edit in utils->database.py on line 3
3. Install Python dependencies using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

### Steps

1. Clone this repository
2. Navigate to the directory

   ```bash
   cd voila-restaurant
   ```

3. Make sure your MongoDB is running
4. To run the application

   ```bash
   python app.py
   ```

5. To run the tests

   ```bash
   python -m pytest
   ```
