from app import db
from app.models import User, Result, Quiz, Question
from datetime import datetime, timedelta
import random
from random import randrange
from sqlalchemy import func, desc
import re


def load_data(filename, sports):
    file = []
    sports_index = 0
    
    with open(filename) as fp:
        line = fp.readline()
        counter = 1
        while line:
            if line == '\n':
                sports_index += 1
            else:
                file.append(line + "?" + sports[sports_index])

            line = fp.readline()
            counter += 1

    return file

def run(user_id):
    questions = load_data('questions.txt', ['NBA', 'Soccer', 'NFL'])

    arr_questions = []
    titles = ["NBA Quiz 1", "NBA Quiz 2", "NBA Quiz 3", "Soccer Quiz 1", "Soccer Quiz 2", "NFL Quiz"]

    #Create Quizzes
    x = 0
    for title in titles:
        global new_sport

        if x < 3:
            new_sport = 'NBA'
        elif x < 5:
            new_sport = 'Soccer'
        else:
            new_sport = 'NFL'
        x += 1

        quiz = Quiz.query.filter_by(title=title).first()
        if quiz:
            continue

        new_quiz = Quiz(title=title, sport=new_sport)

        db.session.add(new_quiz)
        db.session.commit()

    #Create Quiz Questions
    i = 0
    for question in questions:
        arr = question.replace('\n', '').replace('\t', '').split("?", 2)
        arr_questions.append(arr)

        global title2

        if arr_questions[i][2] == 'NBA':
            title2 = random.choice([titles[0], titles[1], titles[2]])
        elif arr_questions[i][2] == "Soccer":
            title2 = random.choice([titles[3], titles[4]])
        elif arr_questions[i][2] == "NFL":
            title2 = titles[5]
        else:
            print('error finding quiz title')
        
        quiz = Quiz.query.filter_by(title=title2).first()

        regex = re.compile(".*?\((.*?)\)")
        answer = re.sub(r'\([^)]*\)', '', arr_questions[i][1])

        new_question = Question(question=arr_questions[i][0], answer=answer, sport=arr_questions[i][2], quiz_id=quiz.id)

        db.session.add(new_question)
        db.session.commit()

        i += 1

    #Create fake results
    def random_date(start, end):
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)


    for a in range(15):
        d1 = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime('1/1/2021 4:50 AM', '%m/%d/%Y %I:%M %p')
        date = random_date(d1, d2)

        rand_title = random.choice(titles)

        rand_quiz = Quiz.query.filter_by(title=rand_title).first()

        num = Question.query.filter(Question.quiz_id == rand_quiz.id).count()
        score = random.randrange(num)

        new_result = Result(date=date, user_id=user_id, score=score, questions_answered=num, quiz_title=rand_title)

        db.session.add(new_result)
        db.session.commit()


