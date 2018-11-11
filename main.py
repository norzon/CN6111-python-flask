from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('pages/index.html')

if __name__ == '__main__':
    app.run(debug=True)
