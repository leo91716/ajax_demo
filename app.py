from flask import Flask, render_template, redirect, url_for, request, jsonify, session,send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys, os

app = Flask(__name__)
db = SQLAlchemy()


# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))

db.init_app(app)


# Models
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    comment = db.Column(db.Text)



@app.route('/')
def index():
    notes=Note.query.all()
    return render_template('index.html',notes=notes)

@app.route('/ajax_comment',methods=['POST'])
def ajax_comment():
    note=Note(**request.form)
    db.session.add(note)
    db.session.commit()
    return jsonify(msg='success')
