from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from utils import gen_draw, combinations, get_flag
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gang = db.Column(db.String(50))
    bankroll = db.Column(db.Integer)
    state = db.Column(db.PickleType)
    draw1 = db.Column(db.PickleType)
    draw2 = db.Column(db.PickleType)
    deck = db.Column(db.PickleType)
    check = db.Column(db.Boolean)
    bet = db.Column(db.Integer)
    i = db.Column(db.PickleType)

with app.app_context():
    db.create_all()

@app.route('/')
def accueil():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    session.clear()
    gang = request.form['gang']
    age = int(request.form['age'])
    bankroll = int(request.form.get('bankroll'))

    gangs = ["grove street", "ballas"]
    error_index = ""
    
    if gang.lower() in gangs:
        if age >= 18:
            if bankroll >= 1 and bankroll <= 10000:
                new_user = User(gang=gang, draw2=[], bankroll=bankroll, state=[])
                db.session.add(new_user)
                db.session.commit()

                session['user_id'] = new_user.id

                return redirect('/bet', 302)
            else:
                return render_template('index.html', error_index="Don't be a tramp")
        else:
            return render_template('index.html', error_index="You are not of legal age")
    else:
        return render_template('index.html', error_index="Other gangs are not accepted")

@app.route('/bet', methods=['GET', 'POST'])
def bet():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('index'))
    if user.bet is not None:
        return redirect(url_for('play'))
    if isinstance(user.bankroll, int) and user.bankroll <= 0:
        return redirect(url_for("a"))
    user.deck = ['2-h', '3-h', '4-h', '5-h', '6-h', '7-h', '8-h', '9-h', '10-h', 'J-h', 'Q-h', 'K-h', 'A-h', '2-d', '3-d', '4-d', '5-d', '6-d', '7-d', '8-d', '9-d', '10-d', 'J-d', 'Q-d', 'K-d', 'A-d', '2-c', '3-c', '4-c', '5-c', '6-c', '7-c', '8-c', '9-c', '10-c', 'J-c', 'Q-c', 'K-c', 'A-c', '2-s', '3-s', '4-s', '5-s', '6-s', '7-s', '8-s', '9-s', '10-s', 'J-s', 'Q-s', 'K-s', 'A-s']
    

    if request.method == "GET":
        user.check = False
        draw1, draw2, state = gen_draw(user.deck, user.state)
        user.draw1 = draw1
        user.draw2 = draw2
        user.state = state
        db.session.commit()
    
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('index'))

    if request.method == "POST":
        try:
            bet = int(request.form.get('bet'))
            if user.bankroll//10 <= bet <= user.bankroll:
                user.bet = bet
                db.session.commit()
                return redirect(url_for('play'))
            else:
                session['error_bet'] = "You can't bet less than 10% or more than your bankroll."
                return render_template('bet.html', bankroll=user.bankroll, error_mise=session['error_bet'])
        except:
            return render_template("bet.html", error_mise="Error type bet!")

    return render_template('bet.html', bankroll=user.bankroll)

@app.route('/play', methods=['GET', 'POST'])
def play():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('index'))

    if user.check == True or user.bet is None:
        return redirect(url_for('bet'))
    if isinstance(user.bankroll, int) and user.bankroll <= 0:
        return redirect(url_for("a"))
    if request.method == "POST":
        user.i = request.form.getlist('i')
        db.session.commit()

        for k in user.i:
            if k not in user.draw1:
                session['error_choice'] = "Please choose a valid card"
                user.i = []
                return render_template('play.html', bankroll=user.bankroll, draw1=user.draw1, bet=user.bet, error_choice=session['error_choice'])

        return redirect(url_for('shuffling'))

    return render_template('play.html', bankroll=user.bankroll, draw1=user.draw1, bet=user.bet)

@app.route('/shuffling', methods=['GET', 'POST'])
def shuffling():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('index'))
    if user.bet is None:
        return redirect(url_for('bet'))
    len_choice = 5 - len(user.i)
    addition = user.draw2[0:len_choice]
    session['drawFinal'] = user.i + addition

    gain, result = combinations(session['drawFinal'], user.bet)
    user.bankroll += gain - user.bet
    user.check = True
    user.bet = None
    session['Bankroll_new'] = user.bankroll
    db.session.commit()

    session['gain'] = gain
    session['result'] = result

    if user.bankroll <= 0:
        return redirect(url_for('Lose'))
    if user.bankroll > 10000000000:
        session['flag'] = get_flag()
        return render_template('flag.html')
    

    return render_template('shuffling.html', bankroll=user.bankroll, drawFinal=session['drawFinal'])

@app.route('/Lose')
def Lose():
    return render_template('Lose.html')

@app.route('/a')
def a():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=21010)
