from flask import *
import hashlib
import mysql.connector
import json
from datetime import timedelta


mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root"
)

db = mydb.cursor()

views = Blueprint('views', __name__)

@views.before_request
def session_lifetime():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=365)



@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="POST":
        username = request.form['username']
        password = request.form['password']

        if len(username) == 0 or len(password) == 0:
            return render_template('login.html', error = "Fill all fields", username=username, password=password)
        if " " in username:
            return render_template('login.html', error = "Username must not contain spaces", username=username, password=password)
        if len(username) > 20:
            return render_template('login.html', error = "Username is too long", username=username, password=password)
        if " " in password:
            return render_template('login.html', error = "Password must not contain spaces", username=username, password=password)
        if len(password) > 20:
            return render_template('login.html', error = "Password is too long", username=username, password=password)
        
        db.execute(f"SELECT * FROM mymatch.users WHERE username = '{username}' and password = '{hashlib.sha256(password.encode()).hexdigest()}';")
        acc = db.fetchone()
        if acc:
            session['username'] = acc[1]
            session['user_id'] = acc[0]
            session.modified = True

            return redirect(url_for('views.mymatches'))
        else:
            return render_template('login.html', error="User not found", username=username, password=password)
    else:
        session.pop('username', None)
        session.pop('user_id', None)
        session.modified = True
        return render_template('login.html')



@views.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method =="POST":
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']


        if len(username) == 0 or len(password1) == 0 or len(password2) == 0:
            return render_template('sign_up.html', error = "Fill all fields", username=username, password1=password1, password2=password2)
        
        if " " in username:
            return render_template('sign_up.html', error = "Username must not contain spaces", username=username, password1=password1, password2=password2)
        if len(username) > 20:
            return render_template('sign_up.html', error = "Username is too long", username=username, password1=password1, password2=password2)
        if password1 != password2:
            return render_template('sign_up.html', error = "Password fields not matching", username=username, password1=password1, password2=password2)
        if " " in password1:
            return render_template('sign_up.html', error = "Password must not contain spaces", username=username, password1=password1, password2=password2)
        if len(password1) > 20:
            return render_template('sign_up.html', error = "Password is too long", username=username, password1=password1, password2=password2)
        
        db.execute(f"SELECT * FROM mymatch.users WHERE username = '{username}';")
        user = db.fetchone()
        if user:
            return render_template('sign_up.html', error = "Username already taken", username=username, password1=password1, password2=password2)

        db.execute(f"INSERT INTO mymatch.users(username, password) VALUES('{username}', '{hashlib.sha256(password1.encode()).hexdigest()}');")
        mydb.commit()

        return redirect(url_for('views.login'))
    else:
        session.pop('username', None)
        session.pop('user_id', None)
        session.modified = True
        return render_template('sign_up.html')



@views.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    session.modified = True
    

    return redirect(url_for('views.login'))



@views.route("/")
def main():
    return redirect(url_for('views.mymatches'))



@views.route("/mymatches", methods=["GET", "POST"])
def mymatches():
    
    if request.method == "POST":
        pass
    else:
        if 'username' in session:
            username = session['username']
            user_id = session['user_id']
            db.execute(f"SELECT person_name, score FROM mymatch.matches WHERE uid = '{user_id}';")
            rows = db.fetchall()

            matches = []
            for row in rows:
                matches.append([row[0], row[1]])

            matches.reverse()
            return render_template("mymatches.html", matches=matches)
        else:
            return redirect(url_for('views.login'))



@views.route("/mymatches/delete")
def delete_match():
    if 'username' in session:
        try:
            match = request.args['match']
        except:
            return redirect(url_for('views.mymatches'))
        else:
            match = request.args['match']

        user_id = session['user_id']

        db.execute(f"DELETE FROM mymatch.matches WHERE uid = '{user_id}' AND person_name = '{match}';")
        mydb.commit()

        return redirect(url_for('views.mymatches'))

    else:
        return redirect(url_for('views.mymatches'))
 


@views.route("/mytypes", methods=["GET", "POST"])
def mytypes():
    user_id = session['user_id']

    if request.method == "POST":
        db.execute(f"SELECT type, val FROM mymatch.types WHERE uid = '{user_id}';")
        rows = db.fetchall()

        types = []
        
        for row in rows:
            types.append([row[0], row[1]])
        types.reverse()

        type = request.form['type']
        val = request.form['val']

        if len(type) == 0 or len(val) == 0:
            return render_template('mytypes.html', error="Fill all fields", type=type, val=val, types=types)
        if not val.isnumeric() or float(val) % 1 != 0:
            return render_template('mytypes.html', error="Weight must be an integer from 1 to 10", type=type, val=val, types=types)
        val = int(val)
        if val > 10 or val < 1:
            return render_template('mytypes.html', error="Weight must be an integer from 1 to 10", type=type, val=val, types=types)
    
        db.execute(f"SELECT * FROM mymatch.types WHERE type = '{type}' AND uid = '{user_id}';")
        type_ = db.fetchone()
        if type_:
            return render_template('mytypes.html', error="Type already exists", type=type, val=val, types=types)

        db.execute(f"INSERT INTO mymatch.types(uid, type, val) VALUES('{session['user_id']}', '{type}', '{val}');")
        mydb.commit()

        return redirect(url_for('views.mytypes'))
    else:
        if 'username' in session:
            
            db.execute(f"SELECT type, val FROM mymatch.types WHERE uid = '{user_id}';")
            rows = db.fetchall()

            types = []
            for row in rows:
                types.append([row[0], row[1]])

            types.reverse()
            return render_template("mytypes.html", types=types)
        else:
            return redirect(url_for('views.login'))

@views.route("/mytypes/delete")
def delete_type():
    if 'username' in session:
        try:
            type = request.args['type']
        except:
            return redirect(url_for('views.mytypes'))
        else:
            type = request.args['type']

        user_id = session['user_id']

        db.execute(f"DELETE FROM mymatch.types WHERE uid = '{user_id}' AND type = '{type}';")
        mydb.commit()

        return redirect(url_for('views.mytypes'))

    else:
        return redirect(url_for('views.mytypes'))
    


@views.route("/new-match", methods=["GET", "POST"])
def new_match():
    user_id = session['user_id']
    if request.method == "POST":
        db.execute(f"SELECT type, val FROM mymatch.types WHERE uid = '{user_id}';")
        rows = db.fetchall()
        
        weights = []
        types = []
        types_ = []
        for row in rows:
            types.append(row[0])
            types_.append(row[0])
            weights.append(row[1])
        name = request.form['name']
        if len(name) == 0:
            return render_template('new_match.html', error="\"Person's Name\" field is empty", types=types_)
        
        db.execute(f"SELECT * FROM mymatch.matches WHERE person_name = '{name}' AND uid = '{user_id}';")
        match = db.fetchone()
        if match:
            return render_template('new_match.html', error="Match already exists", types=types_)
        
        vals = []
        delete = []
        for i in range(len(types)):
            val = request.form[f"val{i}"]
            
            if len(val) == 0:
                delete.append(i)
            else:
                if not val.isnumeric() or float(val) % 1 != 0:
                    return render_template('new_match.html', error="Value must be an integer from 1 to 10", types=types_)
                val = int(val)
                if val > 10 or val < 1:
                    return render_template('new_match.html', error="Value must be an integer from 1 to 10", types=types_)
                vals.append(int(val))

        for i in delete:
            del types[i]
            del weights[i]

        if len(types) < 3:
            return render_template('new_match.html', error="Minimum of 3 Types required", types=types_)

        perfect = 0
        score = 0
        for i in range(len(types)):
            perfect += weights[i]
            score += weights[i] * (vals[i] * 0.1)
        
        score = round((score * 100) / perfect)
        types = json.dumps(types)
        
        db.execute(f"""INSERT INTO mymatch.matches(uid, person_name, score, mytypes, typevals) VALUES('{session["user_id"]}', '{name}', '{score}', '{types}', '{vals}');""")
        mydb.commit()
        return redirect(url_for('views.result', match=name))
        
    else:
        if 'username' in session:
            db.execute(f"SELECT type, val FROM mymatch.types WHERE uid = '{user_id}';")
            rows = db.fetchall()

            types = []
            for row in rows:
                types.append(row[0])

            return render_template("new_match.html", types=types)
        else:
            return redirect(url_for('views.login'))



@views.route("/new-match/result")
def result():
    if 'username' in session:
        try:
            name = request.args['match']
        except:
            return redirect(url_for('views.mymatches'))
        else:
            name = request.args['match']

        user_id = session['user_id']
        db.execute(f"SELECT score FROM mymatch.matches WHERE uid = '{user_id}' AND person_name = '{name}';")
        score = db.fetchone()[0]

        if score == 100:
            msg = f"obs: it has to be a real person." 
        elif score >= 90:
            msg = f'What is this? A Disney movie?'
        elif score >= 80:
            msg = f'BINGO!'
        elif score >= 70:
            msg = f'You and {name} would make great friends!'
        elif score >= 60:
            msg = f"Give {name} a chance. Or not. I really don't care."
        elif score >= 50:
            msg = f"Hey buddy I don't make the rules. It is what it is!"
        elif score >= 40:
            msg = f'{name} is a great match! For someone else... *tap in the back*'
        elif score >= 30:
            msg = f'What made you think this was a good idea?'
        elif score >= 20:
            msg = f'Danger, Danger, Danger.'
        elif score >= 10:
            msg = f'I would keep one eye open around {name} if I were you.'

        return render_template('result.html', score=score, msg=msg)
    else:
        return redirect(url_for('views.new_match'))



@views.route("/delete-account")
def delete_account():
    if 'username' in session:
        user_id = session['user_id']
        db.execute(f"DELETE FROM mymatch.types WHERE uid = '{user_id}';")
        db.execute(f"DELETE FROM mymatch.matches WHERE uid = '{user_id}';")
        db.execute(f"DELETE FROM mymatch.users WHERE id = '{user_id}';")

        mydb.commit()

    return redirect(url_for('views.login'))
    