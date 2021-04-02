# -*- coding: utf-8 -*-
from flask import redirect, render_template, request
from flask import g, Blueprint, flash, url_for, session

from app.services.github import GitHub

blueprint = Blueprint('join', __name__, url_prefix='/join')


@blueprint.route('/')
def join():
    return render_template('join/index.html')
