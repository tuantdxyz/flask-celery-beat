# -*- coding: utf-8 -*-
import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from flask_mail import Mail, Message
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab
from celery.result import AsyncResult

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'mailserverpg01@gmail.com'
app.config['MAIL_PASSWORD'] = 'iyyvfyricnzsoruf'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'mailserverpg01@gmail.com'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'
# app.config['CELERY_TASK_RESULT_EXPIRES'] = 15  # 15 secs remove key redis

# celery schedules
app.config['beat_schedule'] = {
    'summer': {
        'task': 'app.add',
        'schedule': timedelta(seconds=10),
        # 'schedule': crontab(minute=1),
        'args': (random.randint(1, 10), random.randint(11, 20))
    }
    ,
    'play-every-morning': {
            'task': 'app.play_task',
            # 'schedule': timedelta(minutes=1)
            'schedule': timedelta(seconds=12),
        }
    ,
    # 'pause-later': {
    #     'task': 'app.pause_task',
    #     "schedule": timedelta(seconds=20),
    # }
}

# Initialize extensions
mail = Mail(app)

# Initialize Celery
celery = Celery(app.name, backend=app.config['result_backend'], broker=app.config['CELERY_BROKER_URL'], include=['app'])
celery.conf.update(app.config)


@celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    try:
        sender = app.config['MAIL_DEFAULT_SENDER']
        recipient = email_data['to']
        message = email_data['message']
        subject = email_data['subject']

        # inputing the message in the correct order
        msg = Message(subject, sender=sender, recipients=[recipient])
        msg.body = message
        with app.app_context():
            mail.send(msg)
    except Exception as e:
        print(e)


@celery.task
def add(x, y):
    return x + y


@celery.task
def play_task():
    return 'play something'


@celery.task
def pause_task():
    return 'enough fun'

# @celery.task(bind=True)
# def long_task(self):
#     """Background task that runs a long function with progress reports."""
#     verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
#     adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
#     noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
#     message = ''
#     total = random.randint(10, 50)
#     for i in range(total):
#         if not message or random.random() < 0.25:
#             message = '{0} {1} {2}...'.format(random.choice(verb),
#                                               random.choice(adjective),
#                                               random.choice(noun))
#         self.update_state(state='PROGRESS',
#                           meta={'current': i, 'total': total,
#                                 'status': message})
#         time.sleep(1)
#     return {'current': 100, 'total': 100, 'status': 'Task completed!',
#             'result': 42}


def check_status(task_id):
    res = AsyncResult(task_id)
    print(res.ready())
    # print(res)
    # print(res.state)
    return res


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', recipient=session.get('recipient', ''), subject=session.get('subject', ''),
                               content=session.get('content', ''))

    # get value from form submit
    recipient = request.form['recipient']
    subject = request.form['title']
    content = request.form['message']

    # set session
    session['recipient'] = recipient
    session['subject'] = subject
    session['content'] = content

    # send the email
    email_data = {
        'subject': subject,
        'to': recipient,
        'message': content
    }
    if request.form['save'] == 'Send':
        # run process
        # task = send_async_email(email_data)

        # send right away, debug ok with delay
        task = send_async_email.delay(email_data)
    else:
        # send in one minute, not debug with apply_async
        task = send_async_email.apply_async(args=[email_data], countdown=60)
    flash('Sending email to {0} with id: {1}'.format(recipient, task.id))
    return redirect(url_for('index'))


@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    # TODO handle UI/UX (flow invoice)
    task_result = send_async_email.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
