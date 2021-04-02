# -*- coding: utf-8 -*-
import os
import uuid
from flask import redirect, render_template, request
from flask import g, Blueprint, flash, url_for, session
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from app.models import photo as p, user as u
from app.settings import BUCKET_URL
from app.extensions import db, s3

blueprint = Blueprint('art', __name__, url_prefix='/art')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


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
            try:
                response = s3.upload_fileobj(
                    file, 'eddiehub-share-images-bucket', filename,
                    ExtraArgs={'ACL': 'public-read'}
                )
                url = BUCKET_URL + filename
                photo = p.Photo(url, id=id)
                user.photos.append(photo)
                db.session.add(photo)
                db.session.commit()
                photos = p.Photo.query.all()
                return redirect(request.url)
            except Exception as e:
                print(e)
                flash('Error during upload', 'danger')
                return redirect(request.url)

    photos = p.Photo.query.all()
    return render_template('art/index.html', photos=photos)
