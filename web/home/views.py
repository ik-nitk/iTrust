from flask import Blueprint, render_template
import requests

blueprint = Blueprint(
            'home',
             __name__
        )

@blueprint.route("/")
def home_page():
    return render_template("home/index.html")