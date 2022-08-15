# flask-celery-beat
flask celery and beat

# Setup

* cd flask-celery-example
* virtualenv venv
* source venv/bin/activate
(venv) $ pip3 install -r requirements.txt

# Demo

## celery
* run (app.py) --> http://localhost:5000/


## schedule
* celery worker handle task:
![image](https://user-images.githubusercontent.com/74556484/184596170-a5ccd2c8-d564-40b7-89a1-ed08e32ce914.png)

![image](https://user-images.githubusercontent.com/74556484/184596025-cac68069-49cc-4f31-8dca-b513f8abc24d.png)

* celery beat get schedule job
![image](https://user-images.githubusercontent.com/74556484/184596364-8e254045-c119-4183-b069-f6d25a65264c.png)

![image](https://user-images.githubusercontent.com/74556484/184596455-45b86630-aadd-4c5c-8295-dd88654336d9.png)

* Script..
celery -A app.celery flower --port=5555

celery -A app.celery beat --loglevel=info -l debug

celery -A app.celery worker --loglevel=info -l debug

celery -A app.celery beat -s /Users/tuantd/Coding/tuantd/flask-celery-beat/celerybeat-schedule --loglevel=INFO
