# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, session
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

blueprint = Blueprint('home', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home/index.html')
