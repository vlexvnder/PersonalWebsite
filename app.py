from flask import Flask
from morse.morse import morse
from sentiment_analysis.main import sentiment
from main_site.main_site import main_site


app = Flask(__name__)

app.secret_key = "totally secret"

app.register_blueprint(morse, url_prefix='/morse')
app.register_blueprint(sentiment, url_prefix='/sentiment')
app.register_blueprint(main_site, url_prefix='/')




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)