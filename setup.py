# Create config file if none found
from pathlib import Path
config = Path('./flaskblog/config.py')
configTemplate = Path('./flaskblog/config-template.py')
if config.is_file() == False and configTemplate.is_file():
    config.write_text(configTemplate.read_text())



from flaskblog import db
from flaskblog.models import User, Post

# Create database
db.drop_all()
db.create_all()
