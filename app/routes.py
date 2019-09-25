from flask import render_template, flash, redirect, url_for, make_response, Flask
from app import app, db
from app.forms import LoginForm, UploadCheckForm, GetCheckStatusForm, RegistrationForm, DeleteCheckForm, UploadDigitallySignedCheckForm
# from flask_login import current_user
# from flask_login import login_required
from flask_login import login_user
from app.models import User, Check
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from .myutils import check_user
import base64
import os, logging, tempfile
from flask import jsonify
import json
import pickle
import io


@app.route('/')
@app.route('/index')
def index():
    #user = check_user(request)
    if not user:
        return redirect(url_for('login'))
    return render_template('index.html', title='Home', user=user, checks=user.checks)
'''
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        resp = make_response(redirect(next_page))
        username: str = user.username
        resp.set_cookie('uid', base64.b64encode(username.encode()))
        return resp
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('uid', '123', max_age=0)
    return resp


# see http://www.thamizhchelvan.com/python/simple-file-upload-python-flask/


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/uploadCheck")
def uploadCheck():
    user = check_user(request)
    if not user:
        return redirect(url_for('login'))
    form = UploadCheckForm()
    return render_template('upload_check.html', title='Upload a Check', form=form)

@app.route("/ajax/check_status", methods=["POST"])
def ajax_check_status():
    user = check_user(request)
    if not user:
        return redirect(url_for('login'))

    list_checks_tuple = []
    check_ids = request.form.getlist("check_ids[]")
    for id in check_ids:
        check = Check.query.filter_by(id=int(id)).first()
        list_checks_tuple.append((id, check.status, check.user_id, check.amount))
    return jsonify(json.dumps(list_checks_tuple))


@app.route("/handleUploadCheck", methods=['POST'])

def handleUploadCheck():
    user = check_user(request)
    if not user:
        return redirect(url_for('login'))
    app.logger.info('handleUploadCheck')
    form = UploadCheckForm()
    if form.is_submitted():
        photo = form.photo
        password = form.password
        logging.debug('received file name: %s password: %s' % (photo.data.filename, password))
        if photo.data.filename != '':
            app.logger.debug('running on windows')
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, photo.data.filename)
            app.logger.debug('saving file to %s' % path)
            photo.data.save(path)

            check = Check(photo=path, amount=form.amount.data, status="Pending", message=form.message.data,
                          user=user)
            db.session.add(check)
            db.session.commit()

            app.logger.debug('check added. id = ' + str(check.id))

            flash('check added. id = ' + str(check.id))

            if '.zip' in photo.data.filename:
                app.logger.debug('zip file uploaded')
                if os.name == 'nt':
                    cmd = '7z x "%s"' % path
                    if password.data != '':
                        cmd += ' -p"%s"' % password.data
                else:
                    cmd = 'unzip x "%s"' % path
                    if password.data != '':
                        cmd += ' -P "%s"' % password.data
                app.logger.debug('running command %s' % cmd)
                os.system(cmd)
            
    return redirect(url_for('uploadCheck'))

@app.route("/uploadDigitallySignedCheck", methods=['POST', 'GET'])

def uploadDigitallySignedCheck():
    user = check_user(request)
    if not user:
        return redirect(url_for('login'))
    app.logger.info('uploadDigitallySignedCheck')
    form = UploadDigitallySignedCheckForm()
    if form.is_submitted():
        checkBytes = io.BytesIO()
        form.signedCheck.data.save(checkBytes)
        signedCheck = None
        try:
            signedCheck = pickle.loads(checkBytes.getbuffer())
        except pickle.UnpicklingError as error:
            flash('Failed deserializing check. Error - ' + str(error))
            return render_template('upload_digital_check.html', title='Upload a Digitally-Signed Check', form=form)
        db.session.add(signedCheck)
        db.session.commit()
        flash('Check Uploaded Successfully!')


    return render_template('upload_digital_check.html', title='Upload a Digitally-Signed Check', form=form)



@app.route("/getCheckStatus", methods=['GET', 'POST'])

def getCheckStatus():
    user = check_user(request)
    if not user:
        return redirect(url_for('login'))
    form = GetCheckStatusForm()
    check_id = request.args.get('check_id', None)
    if check_id:
        check = Check.query.filter_by(id=check_id).first()
        if check is None:
            flash('Check with ID ' + str(check_id) + ' not found')
            return redirect(url_for('getCheckStatus'))
        flash('Check with ID ' + str(check_id) + ' found. Amount - ' + str(check.amount) +
              '. Message - ' + check.message + '. Status - ' + check.status)
    return render_template('get_check_status.html', title='Get Check Status', form=form)


@app.route("/deleteCheck", methods=['GET', 'POST'])
def deleteCheck():
    user = check_user(request)
    if not user:
        return redirect(url_for('login'))
    form = DeleteCheckForm()
    check_id = form.check_id.data
    if check_id:
        check = Check.query.filter_by(id=check_id, user_id=user.id).first()
        if check is None:
            flash('Check with ID ' + str(check_id) + ' not found')
            return redirect(url_for('deleteCheck'))
        db.session.delete(check)
        db.session.commit()
        flash('Check with ID ' + str(check_id) + ' deleted.')
    return render_template('delete_check.html', title='Delete Check', form=form)
