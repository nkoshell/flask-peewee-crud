from setuptools import setup

setup(
    name='flask-peewee-crud',
    version='0.1.1',
    url='https://github.com/nkoshell/flask-peewee-crud',
    license='MIT',
    author='nkoshell',
    author_email='nikita.koshelev@gmail.com',
    description=('A REST API framework for building CRUD APIs using Flask and peewee '
                 '(forked from sanic_crud https://github.com/Typhon66/sanic_crud)'),
    packages=['flask_peewee_crud', 'flask_peewee_crud.resources'],
    platforms='any',
    install_requires=[
        'peewee>=2.10.2',
        'Flask>=0.12.2',
        'inflect>=0.2.5'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='flask peewee api rest crud'
)
