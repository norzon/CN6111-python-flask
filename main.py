# Imports
from flask import Flask, render_template, url_for
from forms import LoginForm, RegistrationForm
import config
app = Flask(__name__)

# App configuration
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
    return render_template('pages/register.html', title='Register', form=form)

# Register login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('pages/login.html', title='Login', form=form)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
