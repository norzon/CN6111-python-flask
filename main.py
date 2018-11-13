# Imports
from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm
import config

# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret

# Register index route
@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('pages/index.html')

# Register registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('pages/register.html', title='Register', form=form)

# Register login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if True: # This should check if username and password in db
            flash(f'You have successfully loged in as {form.username.data}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username and password combination incorrect', 'danger')
    return render_template('pages/login.html', title='Login', form=form)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
