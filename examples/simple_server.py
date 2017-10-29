from flask import Flask
from flask_peewee_crud import generate_crud
from .model import db, Person


db.create_tables([Person])

app = Flask(__name__)
generate_crud(app, [Person])
app.run(host="0.0.0.0", port=8000, debug=True)
