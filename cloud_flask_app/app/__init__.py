import os
from flask import Flask
from werkzeug.utils import secure_filename

app = Flask(__name__)

from app.views import views, user_views, community_handlers, forsale_handlers, housing_handlers, jobs_handlers, service_handlers