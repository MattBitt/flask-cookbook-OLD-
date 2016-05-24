from flask import Flask

from .models import db

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


# Add the `constants` variable to all Jinja templates.
@app.context_processor
def provide_constants():
    return {"constants": {"TUTORIAL_PART": 1}}

db.init_app(app)