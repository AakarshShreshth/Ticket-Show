from flask import request, render_template, flash, url_for, redirect
from flask import current_app as app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from application.database import db
from application.models import User, Venue, Show


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash("Email already in use.", category="error")
        elif username_exists:
            flash("Username already in use.", category="error")
        elif password1 != password2:
            flash("Password doesn't match!", category="error")
        elif len(username) < 3:
            flash("Username too short.", category="error")
        elif len(password1) < 4:
            flash("Password too short.", category="error")
        elif len(email) < 11:
            flash("Invalid Email.", category="error")
        else:
            new_user = User(username=username, email=email)
            new_user.set_password(password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Account created successfully.', category="success")
            return redirect(url_for('index'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash(f'Welcome {username}', category="success")
            login_user(user)
            if user.is_admin():
                return redirect(url_for('admin'))
            return redirect(url_for('index'))

        flash('Invalid email or password', category="error")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', category="success")
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin():
        flash('You do not have permission to access the admin page.', category="error")
        return redirect(url_for('index'))

    venues = Venue.query.all()
    shows = Show.query.all()
    return render_template('admin.html', venues=venues, shows=shows)


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
