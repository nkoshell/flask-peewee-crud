import codecs
import os
import re

from setuptools import setup

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_REGEXP = re.compile(r"^__version__\s*=\s*[\'\"](.+?)[\'\"]\s*$", re.MULTILINE)


def read(fn):
    with codecs.open(os.path.join(PROJECT_DIR, fn), encoding='utf-8') as f:
        return f.read().strip()


def version():
    try:
        return VERSION_REGEXP.findall(read(os.path.join(PROJECT_DIR, 'flask_peewee_crud', '__init__.py')))[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


vn = version()
url = 'https://github.com/nkoshell/flask-peewee-crud'

setup(
    name='flask-peewee-crud',
    version=vn,
    url=url,
    license='MIT',
    author='nkoshell',
    author_email='nikita.koshelev@gmail.com',
    description=('A REST API framework for building CRUD APIs using Flask and peewee '
                 '(forked from sanic_crud https://github.com/Typhon66/sanic_crud)'),
    long_description=read('README.rst'),
    download_url='{url}/archive/{version}.tar.gz'.format(url=url, version=vn),
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
