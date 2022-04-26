from app import db
from app.models import User, Event, Option, Listing, Match, History
from datetime import datetime, timedelta
import random
import math
from random import randint, uniform
from sqlalchemy import func, desc

def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def run():

    start_date = datetime.strptime('03/14/2022 1:30 PM', '%m/%d/%Y %I:%M %p')
    end_date = datetime.strptime('1/1/2009 4:50 AM', '%m/%d/%Y %I:%M %p')

    for a in range(25):
        
        odds = round(((1/3)*math.sqrt(a)+1)*((random.random()/10)+1), 2)
        amount = random.randint(40, 1000)
        option_id = 1
        option_id_reciprical = 2
        calculated_their_odds = math.floor(((1/(odds-1))+1) * 100) / 100

        i = random.randint(10, 2000)
        date = start_date + timedelta(0, i)
        start_date = date
    
        new_listing = Listing(event_id=1, user_id=1, odds=odds, listers_odds=calculated_their_odds,amount=amount, option_id=option_id, user_return=listers_odds*amount, datetime=date)
        #new_listing_reciprical = Listing(event_id=1, user_id=1, odds=(1/odds+1), amount=amount, option_id=option_id_reciprical, time=a)

        db.session.add(new_listing)
        #db.session.add(new_listing_reciprical)
        db.session.commit()

    start_date = datetime.strptime('03/14/2022 1:30 PM', '%m/%d/%Y %I:%M %p')
    for a in range(25):
        
        odds = round(((-1/3)*math.sqrt(a) + 4)*((random.random()/10)+1), 2)
        amount = random.randint(40, 1000)
        calculated_their_odds = math.floor(((1/(odds-1))+1) * 100) / 100
        option_id = 2

        i = random.randint(10, 2000)
        date = start_date + timedelta(0, i)
        start_date = date

        new_listing = Listing(event_id=1, user_id=1, odds=odds, listers_odds=calculated_their_odds, amount=amount, option_id=option_id, user_return=listers_odds*amount, datetime=date)

        db.session.add(new_listing)
        db.session.commit()


run()


