# -*- coding: utf-8 -*-
from flask import redirect, render_template, request
from flask import g, Blueprint, flash, url_for, session

from app.services.github import GitHub

blueprint = Blueprint('art', __name__, url_prefix='/art')


@blueprint.route('/')
def art():
    return render_template('art/index.html')
