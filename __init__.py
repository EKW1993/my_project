from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from blog.routes import *
from blog.models import *

@app.shell_context_processor
def make_shell_context():
    return { "db": db, "Entry": Entry }

if __name__ == '__main__':
    app.run()
