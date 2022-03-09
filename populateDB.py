from app import db
from app.models import User, Result, Event, Option, Listing
from datetime import datetime, timedelta
import random
import math
from random import randint, uniform
from sqlalchemy import func, desc


def run():
    for a in range(50):
        
        odds = round(((1/3)*math.sqrt(a)+1)*((random.random()/10)+1), 2)
        amount = random.randint(40, 1000)
        option_id = 1
        option_id_reciprical = 2

        new_listing = Listing(event_id=1, user_id=1, odds=odds, amount=amount, option_id=option_id, time=a)
        #new_listing_reciprical = Listing(event_id=1, user_id=1, odds=(1/odds+1), amount=amount, option_id=option_id_reciprical, time=a)

        db.session.add(new_listing)
        #db.session.add(new_listing_reciprical)
        db.session.commit()


    for a in range(50):
        
        odds = round(((-1/3)*math.sqrt(a) + 4)*((random.random()/10)+1), 2)
        amount = random.randint(40, 1000)
        option_id = 2

        new_listing = Listing(event_id=1, user_id=1, odds=odds, amount=amount, option_id=option_id, time=a, datetime=datetime.utcnow())

        db.session.add(new_listing)
        db.session.commit()


run()


