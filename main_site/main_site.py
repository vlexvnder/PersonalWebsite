from flask import Blueprint, render_template
import random


main_site = Blueprint("main_site", __name__, 
    template_folder="templates", 
    static_folder="static", 
    static_url_path="/main_site/static" 
)

sweets = ["chocolate chip cookies", "chocolate cake", "candy", "ice cream", "jelly beans"]

@main_site.route("/")
def index():
    return render_template("main_index.html", sweet = random.choice(sweets))
