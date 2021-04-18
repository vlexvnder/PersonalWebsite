from flask import Flask
from morse.morse import morse
from sentiment_analysis.main import sentiment


app = Flask(__name__)

app.secret_key = "totally secret"

app.register_blueprint(morse, url_prefix='/morse')
app.register_blueprint(sentiment, url_prefix='/sentiment')





if __name__ == "__main__":
    app.run(host='0.0.0.0')