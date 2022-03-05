# sharkstakesllc

# Overview:
This is a git repository for a web application which allows users to quiz themselves on any information, but most notably sports trivia.

Note:
The admin account is simply the user with 'admin' as their username (every username is unique)

The structure of the web app is as follows:
 - The home page (index) allows users to choose a quiz which they want to take, or create a new quiz. It also allows the admin to delete quizzes.
 - If a user chooses to create a quiz they are then redirected to a page which allows them to create questions for the quiz they just created.
 - From the home page a user is able to navigate to the login page where they can either login or be redirected to the registration page, where they can register an account.
 - Once a user has navigated to a quiz page they are able to complete the questions and submit it for marking, where they will receive feedback and their results will be submitted.
 - A user can also navigate to the results page where they are able to see the results of all the quizzes they have completed.
 - A user can also navigate to the stats page where they are able to see some statistics which cover the whole playerbase of the web app.
 - Finally, a user can navigate to their user page to view their account details.


 Architecture:
 The app is using 
 - Flask as a host (written in Python3)
 - Jinja2 in combination with HTML5 to structure content
 - JavaScript and JQuery for client side scripts
 - SQLAlchemy to interact with an SQLite3 database
 - CSS to style the pages

 External Libraries Used:
 - Bootstrap: https://getbootstrap.com/
    - CSS: https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css
    - JS: https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.min.js
    - Icons: https://cdn.jsdelivr.net/npm/bootstrap-icons@1.4.1/font/bootstrap-icons.css

 - JQuery: 
    - JS: https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js

 - Chart.js:https://www.chartjs.org
    - JS: https://cdn.jsdelivr.net/npm/chart.js



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
5. to insert sample data once the web application is running:
    - navigate to the login page (top right corner) and click 'register'
    - register an account with username 'admin'
    - navigate back to the user page by clicking the user icon in the top right and login with your admin account
    - scroll down and click on 'Populate Database'
        - This will provide some quizzes as well as mock results for the admin account

# Testing:
To run the database test cases simply run the following in a command prompt:
- run 'python3 db_test.py'


# Assets:

- Logo: https://vectr.com/tmp/jdrmi8dsl/b199CiH8XW.jpg?width=1000&height=1415.5&select=d6Z7hRFbk,h4RZBQ5Akb,aFHme6dQr&quality=1&source=selection

- Logo 2: https://vectr.com/tmp/a3ASCJXv0g/c3HjXNh4MX.svg?width=1920&height=875.06&select=b1cIS9FkaZ,baGc2ISQF&source=selection

- Wireframe tool: https://cacoo.com/