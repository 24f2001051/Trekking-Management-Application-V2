from flask import Flask
from flask_security import Security
from flask_restful import Api, Resource
from flask_security.utils import hash_password
from flask_cors import CORS