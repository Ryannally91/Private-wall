from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models import user, message
from flask_app.controllers import messages
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('index.html')
    return redirect(f"dashboard/{session['user_id']}")

@app.route('/login', methods=['POST'])
def sign_in():
    data = {
        "email": request.form['email'],
        "password" : request.form['password']
    }
    if not user.User.login(data):
        return redirect('/')
    this_user = user.User.find_by_email(data)
    session['user_id'] = this_user.id
    session['first_name'] = this_user.first_name
    return redirect(f'/dashboard/{this_user.id}')


@app.route('/registration')
def registration_form():
    return render_template('registration.html')

@app.route('/register/user', methods=['POST'])
def register():
    if not user.User.validate_submission(request.form):
        return redirect('/registration')
    
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password' : pw_hash
        }   
    # store user id into session
        session['user_id'] = user.User.register_user(data)
        this_user = user.User.find_by_email(data)
        print(this_user)
        this_user.id   #   Figure this out
        session['first_name'] = this_user.first_name
        return redirect (f"/dashboard/{session['user_id']}")

@app.route('/dashboard/<int:id>')
def home(id):

    return render_template('dashboard.html',  all_users = user.User.get_all_users(), messages = message.Message.get_all_messages(id))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# @app.route('/show_info', methods=["POST"])
# def display():
#     if not user.User.validate_submission(request.form):
#         return redirect('/')
#     session['name'] = request.form["name"]
#     session['location'] = request.form["location"]
#     session['language'] = request.form['language']
#     session['comments'] = request.form['comments']
#     users.append(session)
#     return redirect ('/information') 

# @app.route('/information')
# def show():
#     return render_template('display.html')

# @app.route('/newsubmit')
# def reset():
#     session.clear()
#     return redirect('/')