"""Configuración de la app."""

# Standard libraries
import os

# Flask
from flask import Flask

# Python-dotenv (Third party libraries)
from dotenv import load_dotenv


# Variable `app`
app = Flask(__name__)

# Secret key
app.secret_key = os.getenv("SECRET_KEY")

# Load Python-dotenv
load_dotenv()
