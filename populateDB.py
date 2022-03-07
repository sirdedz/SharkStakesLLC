from app import db
from app.models import User, Result, Event, Option, Listing
from datetime import datetime, timedelta
import random
import math
from random import randint, uniform
from sqlalchemy import func, desc


def run():
    for a in range(50):
        
        odds = ((1/3)*math.sqrt(a))*((random.random()/10)+1)
        amount = random.randint(40, 1000)
        option_id = 1

        new_listing = Listing(event_id=1, user_id=1, odds=odds, amount=amount, option_id=option_id, time=a)

        db.session.add(new_listing)
        db.session.commit()

    for a in range(50):
        
        odds = ((-1/3)*math.sqrt(a) + 4)*((random.random()/10)+1)
        amount = random.randint(40, 1000)
        option_id = 2

        new_listing = Listing(event_id=1, user_id=1, odds=odds, amount=amount, option_id=option_id, time=a)

        db.session.add(new_listing)
        db.session.commit()


run()


