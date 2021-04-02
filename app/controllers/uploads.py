# -*- coding: utf-8 -*-
import functools
import json
import requests

from flask import flash, redirect, render_template, request
from flask import Blueprint, session, url_for, g
from flask import send_from_directory

from app.models.user import User
from app.settings import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, UPLOAD_FOLDER
from app.services.github import GitHub

blueprint = Blueprint('uploads', __name__, url_prefix='/uploads')


@blueprint.route('/<filename>')
def get_file(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )
