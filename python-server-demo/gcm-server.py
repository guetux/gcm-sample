#!/usr/bin/env python
from flask import Flask, request, redirect, url_for, render_template, flash
from redis import Redis
from gcm import GCM
from gcm.gcm import GCMException

with open('api_key.txt') as key:
    API_KEY = key.readline().strip()

r = Redis('localhost')
reg_ids = 'gcm_registered_devices'

app = Flask(__name__)
app.secret_key = 'not_so_secret'

registered_devices = set()

@app.route('/')
def index():
    return render_template('index.html',
        devices=r.scard(reg_ids)
    )

@app.route('/register', methods=['POST'])
def register():
    reg_id = request.form.get('regId')
    if reg_id:
        r.sadd(reg_ids, reg_id)
        return 'You are registered'
    else:
        return 'regId not found', 400

@app.route('/unregister', methods=['POST'])
def unregister():
    reg_id = request.form.get('regId', None)
    if reg_id and reg_id in r.smembers(reg_ids):
        r.srem(reg_ids, reg_id)
        return 'You are unregistered'
    else:
        return 'regId not or not registered', 400

@app.route('/sendAll/', methods=['POST'])
def send_all():
    msg = request.form.get('msg')
    if msg:
        gcm = GCM(API_KEY)
        data = {'msg': msg}
        ids = list(r.smembers(reg_ids))
        try:
            response = gcm.json_request(registration_ids=ids, data=data)
            flash('Your message was sent to %d devices' % r.scard(reg_ids))
        except GCMException as gcme:
            flash(gcme.message)

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')