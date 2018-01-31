#encoding: utf8
from werkzeug.security import generate_password_hash,check_password_hash

from exts import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __tablename__= 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)

    def __init__(self,*args,**kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)

    def checkpassowrd(self,raw_passowrd):
        result = check_password_hash(self.password,raw_passowrd)
        return result



    # def is_authenticated(self):
    #     return True
    #
    # def get_id(self,user_id):
    #     if user_id
    #



class Question(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    question_title = db.Column(db.String(50),nullable=False)
    question_content = db.Column(db.Text,nullable=False)
    question_time = db.Column(db.DateTime)
    question_athr = db.Column(db.String(50),nullable=False)

class Answer(db.Model):
    __tablename__='answer'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    answer_content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default = datetime.now)
    answer_author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    answer_queston_id = db.Column(db.Integer,db.ForeignKey('question.id'))

    question = db.relationship('Question',backref=db.backref('answers',
            order_by=id.desc()))
    author = db.relationship('User',backref = db.backref('answers'))