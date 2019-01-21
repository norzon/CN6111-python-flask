from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import LoginForm, RegistrationForm
from flaskblog.models import User
from flask_login import login_user, current_user, logout_user


# Register index route
@app.route('/')
def index():
    return render_template('pages/index.html')

# Register registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, display_name=form.displayName.data,
            password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You may now log in', 'success')
        return redirect(url_for('login'))
    return render_template('pages/register.html', title='Register', form=form)

# Register login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.rememberMe.data)
            return redirect(url_for('index'))
        else:
            flash('Username and password combination incorrect', 'danger')
    return render_template('pages/login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
