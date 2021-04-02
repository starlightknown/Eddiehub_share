# -*- coding: utf-8 -*-
import os
import uuid
from flask import Blueprint, render_template, session
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from app.models import photo as p, user as u
from app.settings import UPLOAD_FOLDER, URL_PREFIX
from app.extensions import db

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

blueprint = Blueprint('home', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if (session.get('user_id') == None):
            flash('Please login to upload files.', 'danger')
            return redirect(request.url)
        user = u.User.query.filter_by(id=session.get('user_id')).first()
        if (user == None):
            flash('Please login to upload files.', 'danger')
            return redirect(request.url)
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            id = str(uuid.uuid4())
            filename = f'{id}.{ext}'
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            url = URL_PREFIX
            url += url_for(
                'uploaded_file',
                filename=filename
            )
            photo = p.Photo(url, id=id)
            user.photos.append(photo)
            db.session.add(photo)
            db.session.commit()
            return render_template('share/index.html', url=url, uploaded=True)
    return render_template('home/index.html')
