import unittest, os
from app import app, db
from app.models import User, Result, Quiz, Question

class UserModelCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        u1 = User(id=0, firstname='Test', surname='Case', email='tester@mail.com', country='AUS')
        u2 = User(id=1, firstname='Test2', surname='Case', email='tester22@mail.com', country='AUS')

        q1 = Quiz(id=0, title='Test_Quiz', sport='Test_Sport')

        qs1 = Question(id=0, question='Test question', answer='Test answer', sport='Test_Sport', quiz_id=0)

        r1 = Result(quiz_title='Test_Quiz', user_id=0, id=0, score=10, questions_answered=12)

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(q1)
        db.session.add(qs1)
        db.session.add(r1)
        db.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User.query.get(0)
        u.set_password('test')
        self.assertFalse(u.check_password('not_correct'))
        self.assertTrue(u.check_password('test'))

    def test_commit(self):
        u1 = User.query.get(0)
        self.assertFalse(u1.is_committed())

        u2 = User.query.get(1)
        q1 = Quiz.query.first()

        r1 = Result(q1.quiz_title, user_id=u1.id, id=0, score=10, questions_answered=12)
        db.session.add(r1)
        db.session.flush()

        db.session.commit()
        self.assertTrue(u1.is_committed())

    #test all queries used in routes.py
    def test_routes(self):
        id = 0
        u1 = User.query.get(int(id))

        quizzes = Quiz.query.all()
        self.assertIsNotNone(quizzes)

        quiz_title = 'Test_Quiz'
        quiz = Quiz.query.filter_by(title=quiz_title).first()
        self.assertIsNotNone(quiz)

        questions = Question.query.filter(Question.quiz_id==quiz.id).all()
        self.assertIsNotNone(questions)

        results = Result.query.filter(Result.user_id==current_user.id).all()
        self.assertIsNotNone(results)

        quiz_object = Quiz.query.filter_by(title=quiz_title).first()
        quiz_id = quiz_object.id
        self.assertIs(quiz_id, 0)

    #test all queries used in controllers.py
    def test_controllers(self):

        quiz = db.session.query(Result.quiz_title, func.count(Result.id).label('qty')).group_by(Result.quiz_title).order_by(desc('qty')).first()
        self.assertIs(quiz, ['Test_Quiz', 1])

        country = db.session.query(User.country, func.count(User.id).label('qty')).group_by(User.country).order_by(desc('qty')).first()
        self.assertIs(country, 2)