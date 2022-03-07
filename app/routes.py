from app import app, db, models, forms
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from app.controllers import UserController, QuizController, ResultController, StatsController
from werkzeug.urls import url_parse
from werkzeug.datastructures import ImmutableMultiDict

from app.models import User, Event, Option, Result, Listing
from datetime import datetime
import json
import populate_db

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

    for listing in listings:
        new_listing = []

        option = Option.query.filter(Option.id==listing.option_id).first()
        other_options = Option.query.filter(Option.event_id==event.id).filter(Option.id!=listing.option_id).all()

        option_title = option.pick
        listing_id = listing.id
        odds = listing.odds
        amount = listing.amount

        new_listing = {"id": listing_id, "option": option_title, "odds": odds, "amount": amount, "other_options": other_options}


        listings_final.append(new_listing)

    return render_template('event.html', title="Event", event=event, listings=listings_final)



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
        options_dict[option.id] = [option.pick]
    
    #get all listings for the event CHANGE ORDERBY TO DATETIME
    listings = Listing.query.filter(Listing.event_id==event_id).order_by(Listing.id.asc()).all()

    #counter to start at earliest time
    counter = listings[0].id

    for listing in listings:
        options_dict[listing.option_id].append({"odds": listing.odds, "time": listing.time})

    final.append(options_dict)

    return json.dumps(final, default=str)

@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    if current_user.username == 'admin':

        return render_template('user.html')

    return render_template('user.html', title="Results")

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title="About Us")

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