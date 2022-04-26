from app import app, db, models, forms
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app.controllers import UserController, QuizController
from werkzeug.urls import url_parse
from werkzeug.datastructures import ImmutableMultiDict

from app.models import User, Event, Option, Listing, Match, History
from datetime import datetime
import time
import json
import math
import populate_db

import requests

@app.route('/')
@app.route('/index')
def index():

    #Get quizzes for front page
    events = Event.query.all()

    for event in events:

        if len(Listing.query.filter(Listing.event_id==event.id).all()) < 1:

            event.no_listings = True

            continue

        #Get listing with highest odds
        highest_odds_listing = Listing.query.filter(Listing.event_id==event.id).order_by(Listing.odds.desc()).first()

        highest_odds_pick = Option.query.filter(Option.id==highest_odds_listing.option_id).first()

        highest_odds_pick = highest_odds_pick.pick
        highest_odds_amount = highest_odds_listing.amount
        highest_odds = round(highest_odds_listing.odds, 2)

        event.highest_odds = highest_odds
        event.highest_odds_pick = highest_odds_pick
        event.highest_odds_amount = highest_odds_amount

        #Get listing with highest bet amount
        highest_amount_listing = Listing.query.filter(Listing.event_id==event.id).order_by(Listing.amount.desc()).first()

        highest_amount_pick = Option.query.filter(Option.id==highest_amount_listing.option_id).first()

        highest_amount_pick = highest_amount_pick.pick
        highest_amount_odds = round(highest_amount_listing.odds, 2)
        highest_amount = highest_amount_listing.amount

        event.highest_amount_odds = highest_amount_odds
        event.highest_amount_pick = highest_amount_pick
        event.highest_amount = highest_amount

    return render_template('index.html', events=events)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if not current_user.is_authenticated:
        if form.validate_on_submit():
            return UserController.login_post(form)

        return UserController.login(form)


    return redirect(url_for('user'))

@app.route('/logout')
def logout():
    return UserController.logout()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()

    if form.validate_on_submit():
        return UserController.register_post(form)

    return UserController.register(form)



@app.route('/event/<string:event_id>', methods=['GET'])
def event(event_id):

    #return option, odds, amount in listings array
    event = Event.query.filter(Event.id==event_id).first()

    event_title = event.title

    listings = Listing.query.filter(Listing.event_id==event.id).all()

    listings_final = []
    options = Option.query.filter(Option.event_id==event.id).all()

    for option in options:
        best_listing = Listing.query.filter(Listing.option_id==option.id).order_by(Listing.odds.desc()).first()

        if best_listing:
            option.best_odds = best_listing.odds
            option.best_odds_amount = best_listing.amount
        else:
            option.best_odds = 0

    for listing in listings:
        new_listing = []

        user = User.query.filter(User.id==listing.user_id).first()
        username = user.username

        option = Option.query.filter(Option.id==listing.option_id).first()
        option_title = option.pick
        alt_options = Option.query.filter(Option.event_id==event.id).filter(Option.id!=listing.option_id).all()
        other_options = []
        
        for option in alt_options:
            other_options.append(option.pick)

        listing_id = listing.id
        odds = listing.odds
        amount = listing.amount
        daymonth = str(listing.datetime.day) + '/' + str(listing.datetime.month) + " " + str(listing.datetime.hour) + ":" + str(listing.datetime.minute).zfill(2)
        match_amount = math.floor((listing.user_return-listing.amount) * 100) / 100

        new_listing = {"id": listing_id, "pick": option_title, "odds": odds, "amount": amount, "username": username, "daymonth": daymonth, "other_options": other_options, "user_return": listing.user_return, "match_amount": match_amount, "user_id": listing.user_id}

        listings_final.append(new_listing)

    return render_template('event.html', title="Event", event=event, listings=listings_final, options=options)



@app.route('/results', methods=['GET', 'POST'])
@login_required
def results():
    return ResultController.generate()


#route for data to be sent for event graph
@app.route('/get_event_json/<string:event_id>')
def get_event_json(event_id):

    final = []
    options_dict = {}

    #get all options for the event
    options = Option.query.filter(Option.event_id==event_id).all()

    for option in options:
        options_dict[option.id] = [{"pick": option.pick, "colour": option.colour, "accent": option.accentColour}]
        #options_dict[option.id + len(options)] = [{"pick": "Cavs your odds", "colour": "grey", "accent": option.accentColour}]
    
    #get all listings for the event CHANGE ORDERBY TO DATETIME
    listings = Listing.query.filter(Listing.event_id==event_id).order_by(Listing.datetime.asc()).all()

    if len(listings) > 0:
        for listing in listings:
            index = listing.option_id + len(options)
            recip_odds = (1/listing.odds)+1

            #indexed to the other option as to show on graph from matching user's perspective
            if listing.option_id == 1:
                index = 2
            elif listing.option_id == 2:
                index = 1

            options_dict[index].append({"odds": listing.odds, "time": listing.datetime})
            #options_dict[index].append({"odds": recip_odds, "time": listing.time})

        final.append(options_dict)

    
    return json.dumps(final, default=str)

@app.route('/post_listing', methods=['POST'])
@login_required
def post_listing():
    jsonData = request.get_json(force=True)

    #Get specific data
    event_id = int(jsonData[0]["event_id"])
    user_id = int(jsonData[0]["user_id"])
    option_id = int(jsonData[0]["option_id"])
    user_odds = float(jsonData[0]["user_odds"])
    their_odds = float(jsonData[0]["their_odds"])
    amount = float(jsonData[0]["amount"])
    listing_return = float(jsonData[0]["listing_return"])

    msg = {
        'event_id': event_id,
    }

    #Check all data is present
    if 'event_id' not in jsonData[0] or 'user_id' not in jsonData[0] or 'option_id' not in jsonData[0] or 'user_odds' not in jsonData[0] or 'their_odds' not in jsonData[0] or 'amount' not in jsonData[0] or 'listing_return' not in jsonData[0]:
        msg['result'] = 'failure'
        msg['error'] = "Internal Server Error."

        return msg

    #Check if user_id is the same as the user logged in
    if not current_user.id == user_id:
        msg['result'] = 'failure'
        msg['error'] = "User ID's dont match!"

        return msg

    #Check the user has the required balance
    user = User.query.filter(User.id==current_user.id).first()
    user_balance = user.balance

    if not user_balance >= amount:
        msg['result'] = 'failure'
        msg['error'] = "Balance not sufficient!"

        return msg

    #check that the odds are validated
    if user_odds < 1 or their_odds < 1 or amount < 1:
        msg['result'] = 'failure'
        msg['error'] = "Odds are invalid"

        return msg

    calculated_their_odds = math.floor(((1/(user_odds-1))+1) * 100) / 100
    if user_odds * amount != listing_return or their_odds != calculated_their_odds:
        msg['result'] = 'failure'
        msg['error'] = "Odds do not match"

        return msg


    #Remove bet amount from user
    current_user.balance -= amount

    #Add new listing to DB
    new_listing = Listing(event_id=event_id, odds=their_odds, listers_odds=user_odds, amount=amount, option_id=option_id, user_id=user_id, datetime=datetime.utcnow(), user_return=listing_return)
    db.session.add(new_listing)
    db.session.commit()
    
    msg['result'] = 'success'

    return msg

@app.route('/match_listing', methods=['POST'])
@login_required
def match_listing():
    jsonData = request.get_json(force=True)

    #Get specific data
    listing_id = int(jsonData[0]['listing_id'])
    user_id = int(jsonData[0]['user_id'])

    msg = {
    }

    #Check that the message was received
    if not isinstance(listing_id, int) or not isinstance(user_id, int) or 'user_id' not in jsonData[0] or 'listing_id' not in jsonData[0]:
        msg['result'] = 'failure'
        msg['error'] = "Internal Error"

        return msg

    #Check if user_id is the same as the user logged in
    if not current_user.id == user_id:
        msg['result'] = 'failure'
        msg['error'] = "User ID's dont match!"

        return msg

    #Check the listing still exists
    listing = Listing.query.filter(Listing.id==listing_id).first()
    if listing.matched:
        msg['result'] = 'failure'
        msg['error'] = "Listing already matched"

        return msg

    #Check the user has the required balance
    user = User.query.filter(User.id==current_user.id).first()
    user_balance = user.balance

    if not user_balance >= (listing.user_return - listing.amount):
        msg['result'] = 'failure'
        msg['error'] = "Balance not sufficient!"

        return msg

    #Remove bet amount from user
    current_user.balance -= (listing.user_return - listing.amount)

    #Add new match to DB and update listing to be matched
    new_match = Match(user_listing_id=listing.user_id, user_matching_id=current_user.id)
    db.session.add(new_match)
    listing.matched = True
    db.session.commit()
    
    msg['result'] = 'success'

    return msg


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    
    
    #if current_user.username == 'admin':
    #    #Do admin things
    #    return render_template('user.html')

    #Get all listings for user
    #Perhaps sort by event time later
    user_listings = Listing.query.filter(Listing.user_id==current_user.id).order_by(Listing.datetime.asc()).all()

    for listing in user_listings:
        event = Event.query.filter(Event.id==listing.event_id).first()
        listing.event = event.title
        #listing.event_datetime = event.datetime

        option = Option.query.filter(Option.id==listing.option_id).first()
        listing.pick = option.pick
        #listing.their_pick = option.their_pick

        listing.daymonth = str(listing.datetime.day) + '/' + str(listing.datetime.month) + " " + str(listing.datetime.hour) + ":" + str(listing.datetime.minute).zfill(2)


    return render_template('user.html', listings=user_listings)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title="About Us")


@login_required
@app.route('/bank', methods=['GET'])
def bank():


    result = []

    user = User.query.filter(User.id==current_user.id).first()


    return render_template('bank.html', title='Bank')



@login_required
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():

    amount = request.args.get('amount', default=5, type = int)

    api_key = 'Uznvgn9Tb1rOgO47kNy88CEhXSuBzTUH2Md2cbfyp4Q';
    url = 'https://www.blockonomics.co/api/new_address';

    headers = {'Authorization': "Bearer " + api_key}
    r = requests.post(url, headers=headers)
    if r.status_code == 200:
        address = r.json()['address']
        print ('Payment receiving address ' + address)

    else:
        print(r.status_code, r.text)

    return render_template('bank.html', title='Bank')


@app.route('/payment_callback', methods=['GET', 'POST'])
def payment_callback():

    status = request.args.get('status', default=5, type = int)
    addr = request.args.get('addr', default=5, type = int)
    value = request.args.get('value', default=5, type = int)
    txid = request.args.get('txid', default=5, type = int)

    price_data = requests.get('https://www.blockonomics.co/api/price?currency=USD')
    USDBTC = price_data.json()['price']

    price_USD = (value * 0.00000001) * USDBTC

    print('received funds: USD' + str(price_USD) + ', BTC' + str(value * 0.00000001))

    return 'success'






















##REDACTED --------------------------------------------------------------
@app.route('/content', methods=['GET', 'POST'])
def content():
    return render_template('content.html', title="Learning Materials")

@app.route('/stats', methods=['GET'])
def stats():
    return StatsController.get()

@app.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if current_user.username == 'admin':

        form = forms.CreateQuizForm()

        if form.validate_on_submit():
            return QuizController.create(form)

        return render_template('create_quiz.html', title="Create A Quiz", form=form)
    else:
        return redirect('index')

@app.route('/create_question/<string:quiz_title>', methods=['GET', 'POST'])
@login_required
def create_question(quiz_title):
    if current_user.username == 'admin':

        form = forms.CreateQuestionForm()

        quiz_object = Quiz.query.filter_by(title=quiz_title).first()
        quiz_id = quiz_object.id

        questions = Question.query.filter(Question.quiz_id==quiz_id).all()

        if form.validate_on_submit():
            return QuizController.createQuestion(form, quiz_title)

        return render_template('create_question.html', title="Create A Question", form=form, questions=questions, quiz=quiz_object)
    else:
        return redirect('index')


@app.route('/delete_quiz/<string:title>', methods=['GET', 'POST'])
@login_required
def delete_quiz(title):
    if current_user.username == 'admin':

        quiz_object = Quiz.query.filter_by(title=title).first()
        quiz_id = quiz_object.id

        db.session.query(Question).filter(Question.quiz_id==quiz_id).delete()
        db.session.query(Result).filter(Result.quiz_title==quiz_object.title).delete()
        
        db.session.delete(quiz_object)
        db.session.commit()

    
    return redirect('/')


@app.route('/submit_quiz', methods=['GET', 'POST'])
@login_required
def submit_quiz():

    jsonResult = request.get_json(force=True)
    quiz_title = jsonResult[0]['title']

    #Get actual quiz answers from database for marking
    quiz_object = Quiz.query.filter_by(title=quiz_title).first()

    marking_questions = Question.query.filter(Question.quiz_id==quiz_object.id).all()
    score = 0
    questions_answered = 0
    result = {}

    for x in range(len(jsonResult)-1):
        m = marking_questions[x].answer.replace(" ", '').lower()
        u = jsonResult[x+1]['answer'].replace(" ", '').lower()

        if m == u:
            #Correct answer
            score += 1
        
        result[marking_questions[x].question] = [marking_questions[x].answer, jsonResult[x+1]['answer']]
            
        questions_answered += 1


    result['score'] = [score, questions_answered]
    new_result = Result(score=score, questions_answered=questions_answered, user_id=current_user.id, quiz_title=quiz_title, date=datetime.utcnow())

    db.session.add(new_result)
    db.session.commit()
    
    return json.dumps(result, default=str)


@app.route('/populate')
@login_required
def populate():
    if current_user.username == 'admin':
        populate_db.run(current_user.id)

    return redirect('index')