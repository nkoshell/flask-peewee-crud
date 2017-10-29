from peewee import SqliteDatabase, Model, CharField, DateTimeField, IntegerField, ForeignKeyField
from flask import Flask
import datetime

from flask_peewee_crud import generate_crud

db = SqliteDatabase('dev_data.db')


class BaseModel(Model):
    class Meta:
        database = db


class Job(BaseModel):
    name = CharField()
    description = CharField()
    base_pay = IntegerField()


class Person(BaseModel):
    name = CharField()
    job = ForeignKeyField(Job, related_name="person_job", null=True)
    email = CharField()
    create_datetime = DateTimeField(default=datetime.datetime.now, null=True)


# if there is an error DB already exists
try:
    db.create_tables([Person, Job])
    job = Job(name='Space garbage man', description='Collects garbage in space', base_pay=15)
    person = Person(name='Sanic the Hedgehog', email='gottagofeast@fast.com', job=1)
    job.save()
    person.save()
except Exception:
    pass

app = Flask(__name__)

generate_crud(app, [Person, Job])
app.run(host='0.0.0.0', port=8000, debug=True)
