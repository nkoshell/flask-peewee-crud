flask-peewee-crud
=================

|PyPI| |PyPI version|


``flask-peewee-crud`` forked from `sanic_crud <https://github.com/Typhon66/sanic_crud>`_

``flask-peewee-crud`` is a REST API framework for creating a CRUD (Create/Retrieve/Update/Delete) API using `Flask <http://flask.pocoo.org/>`_ and `PeeWee <http://docs.peewee-orm.com/en/latest/>`_
You can use ``flask-peewee-crud`` to automatically create an API from your PeeWee models, see how it works in the `Documentation <docs/using_a_flask_peewee_crud_api.md>`_

Contributions to the repository are welcome!

Example
-------

.. code:: python

    from peewee import CharField, DateTimeField, SqliteDatabase, Model
    import datetime
    from flask import Flask
    from flask_peewee_crud import generate_crud
    
    db = SqliteDatabase('my_app.db')
    
    class BaseModel(Model):
        class Meta:
            database = db
    
    class Person(BaseModel):
        name = CharField()
        email = CharField()
        create_datetime = DateTimeField(default=datetime.datetime.now, null=True)
    
    db.create_tables([Person])
    
    app = Flask(__name__)
    generate_crud(app, [Person])
    app.run(host="0.0.0.0", port=8000, debug=True)

Installation
------------

-  `python -m pip install flask-peewee-crud`

Documentation
-------------

Documentation can be found in the ``docs`` directory.

.. |PyPI| image:: https://img.shields.io/pypi/v/flask-peewee-crud.svg
   :target: https://pypi.python.org/pypi/flask-peewee-crud/
.. |PyPI version| image:: https://img.shields.io/pypi/pyversions/flask-peewee-crud.svg
   :target: https://pypi.python.org/pypi/flask-peewee-crud/

TODO
----

* `See Issues <https://github.com/nkoshell/flask-peewee-crud/issues>`_
