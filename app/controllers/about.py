# -*- coding: utf-8 -*-
from flask import redirect, render_template, request
from flask import g, Blueprint, flash, url_for, session

from app.services.github import GitHub

blueprint = Blueprint('about', __name__, url_prefix='/about')


@blueprint.route('/')
def about():
    return render_template('about/index.html')
