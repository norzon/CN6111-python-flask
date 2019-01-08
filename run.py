from flaskblog import app
from flaskblog import config

# Run app
if __name__ == '__main__':
    app.run(debug=config.debug)
