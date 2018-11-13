from flask import Flask, render_template, url_for
import config
app = Flask(__name__)

app.config['SECRET_KEY'] = config.secret

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('pages/index.html')

if __name__ == '__main__':
    app.run(debug=True)
