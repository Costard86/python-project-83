from flask import Flask, render_template
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')
