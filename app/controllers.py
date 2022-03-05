#corresponding controller actions to be used in routes.py


from app import forms, models, db, app
from flask import render_template, flash, redirect, request, url_for
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Quiz, Question, Result

from sqlalchemy import func, desc
from dateutil import parser
from datetime import date

#controller class for user functionality
class UserController():

#render login form
    def login(form):

        return render_template('login.html', title='Login', form=form)

#check that username is valid and then check password
#show error/redirect appropriately
    def login_post(form):

        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('user'))

#function for loggin out as user
    def logout():
        logout_user()
        return redirect(url_for('index'))

#render registration form
    def register(form):

        users = User.query.all()

        return render_template('register.html', title='Register', users=users, form=form)

#get info from user table
    def register_post(form):

        username = request.form.get('username')
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        surname = request.form.get('surname')
        dob = request.form.get('dob')
        address = request.form.get('address')
        country = request.form.get('country')
        postcode = request.form.get('postcode')
        state = request.form.get('state')
        phone = request.form.get('phone')
        password = request.form.get('password')

        dob = parser.parse(dob).date()

        user = User.query.filter_by(username=username).first()

        #user will return not None if a user with that username already exists
        if user:
            flash('Username is already in use')
            return redirect(url_for('register'))

        #otherwise create a new database entry
        new_user = User(username=username, email=email, firstname=firstname, surname=surname, dob=dob, address=address, country=country, postcode=postcode, state=state, phone=phone)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

#controller class for quiz
class QuizController():
    #controller for creating a new quiz form or adding to an existing one
    def create(form):

        title = request.form.get('title')
        sport = request.form.get('sport')

        quiz = Quiz.query.filter_by(title=title).first()

        if quiz:
            flash('Quiz already exists, add questions:')
            return redirect(url_for('create_question', quiz_title=title))

        new_quiz = Quiz(title=title, sport=sport)
        db.session.add(new_quiz)
        db.session.commit()

        return redirect(url_for('create_question', quiz_title=title))

#controller for creating questions to then be added into db
    def createQuestion(form, quiz_title):

        quiz = Quiz.query.filter_by(title=quiz_title).first()

        question = request.form.get('question')
        answer = request.form.get('answer')

        new_question = Question(question=question, answer=answer, quiz_id=quiz.id)

        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for('create_question', quiz_title=quiz_title))

#controller class for generating results template
class ResultController():
    def generate():
        results = Result.query.filter(Result.user_id==current_user.id).all()

        return render_template('results.html', title="Results", results=results)


class StatsController():
    def get():

        results = Result.query.all()

#intitialize results for specific user
        class Results():
            def __init__(self, avg, your_avg, pop_quiz, times_played, country, users, avg_age):
                self.avg = avg
                self.your_avg = your_avg
                self.pop_quiz = pop_quiz
                self.times_played = times_played
                self.country = country
                self.users = users
                self.avg_age = avg_age


        #Get averages
        avg = 0

        count = 0
        for r in results:
            if r.questions_answered > 0:
                percentage = (r.score / r.questions_answered) * 100

                avg += percentage
                count += 1

        if count > 0:
            avg = round(avg / count, 2)

        your_avg = 0
        count2 = 0
        if current_user.is_authenticated:
            your_results = Result.query.filter(Result.user_id==current_user.id).all()

            for r in your_results:
                if r.questions_answered > 0:
                    percentage = (r.score / r.questions_answered) * 100

                    your_avg += percentage
                    count2 += 1

            if count2 > 0:
                your_avg = round(your_avg / count2, 2)


        avg_age = 0
        count3 = 0
        users = User.query.filter().all()

        for u in users:
            if u.dob is not None:
                dob = u.dob

                age = date.today() - dob
                age = age.days / 365.25

                avg_age += age
                count3 += 1

        if count3 > 0:
            avg_age = round(avg_age / count3, 2)


        #Get most common fields
        quiz = db.session.query(Result.quiz_title, func.count(Result.id).label('qty')).group_by(Result.quiz_title).order_by(desc('qty')).first()

        country = db.session.query(User.country, func.count(User.id).label('qty')).group_by(User.country).order_by(desc('qty')).first()

        if len(results) != 0:
            results = Results(avg, your_avg, quiz[0], quiz[1], country[0], country[1], avg_age)

            return render_template('stats.html', title="Global Statistics", results=results)


        return render_template('stats.html', title="Global Statistics", results="None")