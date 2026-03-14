from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect

from config import DevelopmentConfig
from models import db
from pizzeria import pizzeria as pizzeria_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
csrf = CSRFProtect(app)

app.register_blueprint(pizzeria_bp)


@app.route("/")
def home():
    return redirect(url_for("pizzeria.index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)