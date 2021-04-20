from flask import Blueprint, render_template
import random


main_site = Blueprint("main_site", __name__, 
    template_folder="templates", 
    static_folder="static", 
    static_url_path="/main_site/static" 
)

veggies = ["lettuce", "beets", "broccoli", "brussel sprouts" ]
sweets = ["chocolate chip cookies", "chocolate cake", "ice cream", "jelly beans", "snickerdoodles"]
sweets2 = ["gummy bears", "gummy worms", "cotton candy", "taffy"]

@main_site.route("/")
def index():
    return render_template("main_index.html", veggie = random.choice(veggies), sweet = random.choice(sweets), sweet2 = random.choice(sweets2))
