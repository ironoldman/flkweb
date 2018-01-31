# encoding:utf-8
from flask import Flask,render_template,request,redirect,url_for,session,app,g,jsonify
from models import User,Question,Answer
import config
from exts import db
from datetime import datetime
from flask.ext.login import login_required,LoginManager
from sqlalchemy import or_
import json

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def index():
    context ={ 'questions':Question.query.filter().order_by('-question_time').all()}
    return render_template('index.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        a = request.get_data()
        print a
        data = json.loads(a)
        telephone = data['telephone']
        password = data['password']
        # telephone = request.form.get('telephone')
        # password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone ).first()
        if user and user.checkpassowrd(password):
            session['user_id'] = user.id
            session.permanent = True
            return jsonify({'r':0,'rs':'ok'})
            # return redirect(url_for('index'))
        else:
            error= 'username or password error'
            print error
            return jsonify({'r': 1,'error':error})
            return u'手机号码错误'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method=='GET':
        return  render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get("password1")
        password2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'此号码已注册'
        elif password1 != password1:
            return u'两次密码不一致'
        else:
            user = User(telephone = telephone,username= username,password = password1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))

@app.route('/logout/')
@login_required
def logout():
    # login_manager.logout_user()
    session.pop('user_id')
    return redirect(url_for('index'))

@app.route('/logind/')
def logind():
    return render_template('logind.html')


@app.route('/question/',methods=['GET','POST'])
def question():
    if session.get('user_id'):
        if request.method == 'GET':
            return render_template('question.html')
        else:
            user_id = session.get('user_id')
            # user = User.query.filter(User.id == user_id ).first()
            user=g.user
            username = user.username
            q_title = request.form.get('title')
            q_content = request.form.get('content')
            question = Question(question_title = q_title,question_content = q_content,
                                question_athr = username,
                                question_time = datetime.now())
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/answer/',methods=['POST'])
@login_required
def answer():
    content = request.form.get('answer')
    user_id = session.get('user_id')
    answer = Answer(answer_content = content)
    # answer.author = User.query.filter(User.id == user_id).first()
    answer.author = g.user
    question_id = request.form.get('question_id')
    answer.question = Question.query.filter(Question.id == question_id).first()
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',detail_id = question_id))

@app.route('/sreach/')
def sreach():
    sreach_value = request.args.get('q')
    questions = Question.query.filter(or_(Question.question_title.contains(sreach_value),
                                          Question.question_content.contains(sreach_value)))\
                                        .order_by('-question_time')
    return render_template('index.html' ,questions = questions)


@app.route('/detail/<detail_id>')
def detail(detail_id):
    question_model = Question.query.filter(Question.id == detail_id).first()
    return render_template('detail.html',question = question_model)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    g.user = User.query.filter(User.id == user_id).first()

@app.context_processor
def my_context_processor():
    # user_id = session.get('user_id')
    # if user_id:
    #     user = User.query.filter(User.id == user_id).first()
    #     if user:
    #         return {'user' : user}
    # return {}
    if g.user:
        return {'user':g.user}
    return {}

@login_manager.user_loader
def load_user(user_id):
    # print '11111'
    return User.query.get(int(user_id))
    # return User.get_id(user_id)



if __name__ == '__main__':
    # # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_wiew = url_for('login')
    app.run(ssl_context='adhoc')
    #app.run()
