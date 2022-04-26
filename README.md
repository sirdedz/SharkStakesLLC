# sharkstakesllc

# Overview: STILL IN EARLY DEVELOPMENT STAGES
This is a git repository for a web application in development for open-market event betting where users can create listings with their own stakes and odds, and other users are able to match these listings to create a bet.


The structure of the web app is as follows:
 - The home page (index) shows upcoming events and allows users to navigate to specific events' page
 - The event page shows all listings for a specific event, including a line graph which shows the odds listed over time for each outcome (the reciprical to show the user's available odds to match an existing listing)
    - The user is able to sort the listings by any of the available metrics, and by outcome seperately
 - The Login/Registration page allows the user to login to an existing account, or register and create an account
 - The User page allows the user to see their details, as well as any existing listings, matches yet to be resulted and previous resulted bets
 - The sports page will feature categories of events to navigate and find specific events
 - Payment system currently uses the Blockonomics API to verify BTC payments have been processed (STILL UNDER CONSTRUCTION)


 Architecture:
 The app is using 
 - Flask as a host (written in Python3)
 - Jinja2 in combination with HTML5 to structure content
 - JavaScript and JQuery for client side scripts
 - SQLAlchemy to interact with an SQLite3 database
 - CSS to style the pages
 - Blockonimcs API for BTC payments

 External Libraries Used:
 - Bootstrap: https://getbootstrap.com/
    - CSS: https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css
    - JS: https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.min.js
    - Icons: https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css

 - JQuery: 
    - JS: https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js

 - Chart.js:https://www.chartjs.org
    - JS: https://cdn.jsdelivr.net/npm/chart.js

- Sorttable



# Instructions for starting web application:
1. navigate to the web application root directory in a command prompt
2. run the following in the command prompt:
    - run 'FLASK_APP=sharkstakes.py'
    - run 'export SECRET_KEY="temp_key"'
3. run the following in the command prompt to initialize the database:
    - run 'sqlite3 app.db'
    - run '.tables'
    - run '.quit'
    - run 'flask shell'
    - run 'from app import db'
    - run 'from app.models import User, Result, Quiz, Question'
    - run 'db.create_all()'
    - run 'quit()'
4. start the application by running the following in a command prompt:
    - run 'flask run'


# Testing: (STILL UNDER CONSTRUCTION)
To run the database test cases simply run the following in a command prompt:
- run 'python3 db_test.py'


# Assets:

- Logo: https://vectr.com/tmp/jdrmi8dsl/b199CiH8XW.jpg?width=1000&height=1415.5&select=d6Z7hRFbk,h4RZBQ5Akb,aFHme6dQr&quality=1&source=selection

- Logo 2: https://vectr.com/tmp/a3ASCJXv0g/c3HjXNh4MX.svg?width=1920&height=875.06&select=b1cIS9FkaZ,baGc2ISQF&source=selection

- Wireframe tool: https://cacoo.com/