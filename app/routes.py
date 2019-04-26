# -*- coding: utf-8 -*-
from flask import render_template, request,redirect, url_for, send_file, flash, abort, Response
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse
from werkzeug import secure_filename

from app import app, db
from app.models import Datafiles, Users
from app.forms import LoginForm, UploadForm
from app.errors import page_not_found

import pytz

from datetime import datetime, timedelta

from io import BytesIO


@app.route('/', methods = ['POST', 'GET'])
@app.route('/index', methods = ['POST', 'GET'])
@login_required
def index():
    form = UploadForm()
    if form.validate_on_submit():
        filename = None
        user_id = None
        if form.datafile.data:
            filename = secure_filename(form.datafile.data.filename)
            if current_user.is_authenticated:
                user_id = current_user.id
        file = Datafiles(
            user_id=user_id,
            filename=filename,
            datafile=form.datafile.data.read(),
            expire=datetime.now(pytz.utc) + timedelta(minutes=form.availability.data)
            )
        db.session.add(file)
        db.session.commit()
        Datafiles.last_commit = datetime.now(pytz.utc)

    return render_template('index.html',form=form)


@app.route('/files', methods = ['POST', 'GET'])
@login_required
def files():
    def delete_expired():
        """Procedure deletes obslete entries in case if database trigger 
        was activated too long ago
        trigger activated after each insert to datafiles
        Useful to keep list of user available files updated list in low load
        can be comented out from code if insertions are frequent enough
        (i.e. trigger activated frequent enough)
        """
        if Datafiles.last_commit:
            print('last commit ',Datafiles.last_commit, 'now: ', datetime.now(pytz.utc))
            print(datetime.now(pytz.utc)-Datafiles.last_commit)
        if Datafiles.last_commit and\
            datetime.now(pytz.utc)-Datafiles.last_commit > timedelta(minutes=1):
            expired = Datafiles.query.filter(
                Datafiles.expire<=datetime.now(pytz.utc)
                ).all()
            for file in expired:
                db.session.delete(file)
            db.session.commit()
            Datafiles.last_commit = datetime.now(pytz.utc)

    if 'lines' in request.args:
        delete_expired()
        files=Datafiles.query.filter(Datafiles.user_id==current_user.id).all()
        if len(files) == 0:
            abort(404)
        return render_template('lines.html', files=files)
    return render_template('files.html', user=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('files'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/file/<file_id>')
@login_required
def file(file_id):
    datafile = Datafiles.query.filter_by(user_id=current_user.id)\
        .filter_by(id=file_id).first()
    return render_template('file_page.html', file=datafile, datetime=datetime)

@app.route('/download/<filename>')
@login_required
def download(filename):
    datafile = Datafiles.query.filter_by(user_id=current_user.id)\
        .filter_by(filename=filename).first()
    return send_file(BytesIO(datafile.datafile),
        attachment_filename=datafile.filename, as_attachment=True)

@app.route('/404/<err>')
def not_found_error(err='No page found'):
    if err == 'file':
        err = '404  No files found'
    return render_template('404.html',error=err), 404