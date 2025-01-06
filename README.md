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
2. MongoDB running locally or on a server. Currently configured like this: mongodb://localhost:27017/. Can edit in utils->database.py on line 12
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

### Pictures
1. Initial Start

![intial](https://github.com/user-attachments/assets/2be1990f-88a2-4e5d-8537-355d6f065fc5)

2. Adding a new visitor to the waitlist

![adding a new visitor to the waitlist](https://github.com/user-attachments/assets/499370ae-1c1e-4843-8a6b-655b52ea382a)

3. Adding watilisted people to confirmed guests

![adding watilisted people to confirmed guests](https://github.com/user-attachments/assets/b475248f-1903-42fd-b275-a506fb9d1aa6)

4. Display analytics

![Display analytics](https://github.com/user-attachments/assets/c5396d94-f793-48fc-b36a-ea4b8a9db1b7)

5. A rough high level system design flow chart

   
![Diagram](https://github.com/user-attachments/assets/30dc13ba-ada8-4091-8ffc-591e964d896b)


### Final Words
I have added comments to each function to show what I was thinking and the logic behind it. You can play around with the app to see all the outputs, you can change the maxCapacity variable on line 57 to a different number. Can also put wrong inputs to see some input validation that I made.

This version was just made to have 1 running application, but I included a rough high level sketch up of a more scalable app.

I chose MongoDB for the scalability and the fact that we do not really need any relationships between our tables. I chose python just because I am most comfortable with it and for the sake of the interview, but for an actual app like this a stack like Node.JS, TypeScript, Express.JS, React (or any other front end frameworks) would be my first choice for an app of this sort. Thanks!
