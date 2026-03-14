from flask import Blueprint

pizzeria = Blueprint("pizzeria", __name__, template_folder="../templates")

from . import routes