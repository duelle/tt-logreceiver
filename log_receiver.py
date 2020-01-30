from flask import Flask, escape, make_response, request, send_file
from flask_api import status
import json
import datetime
import time
import urllib.request
import tempfile
import os

app = Flask(__name__)
tempdir = tempfile.mkdtemp(prefix='tt_logreceiver_')
print('tempdir is: ' + tempdir)
log_header = 'uuid;datetime_triggered;datetime_started;datetime_finished;build_id;job_id;startup_duration;build_url;job_url'

@app.route('/build/triggered/', methods=['POST'])
def build_triggered():
  now = datetime.datetime.now()
  build_uuid = request.form['build_uuid'].strip()

  line = str(now) + 'triggered'

  with open(tempdir + os.sep + build_uuid + '.csv', 'a') as log_file:
    log_file.write(log_header + '\n')
    log_file.write(str(build_uuid) + ';"' + str(now) + '";')

  return line, status.HTTP_200_OK


@app.route('/job/started/', methods=['POST'])
def job_started():
  now = datetime.datetime.now()

  build_uuid = request.form['build_uuid'].strip()

  with open(tempdir + os.sep + build_uuid + '.csv', 'a') as log_file:
    log_file.write('"' + str(now) + '";')

  return line, status.HTTP_200_OK


@app.route('/job/finished/', methods=['POST'])
def job_finished():
  now = datetime.datetime.now()

  build_uuid = request.form['build_uuid'].strip()
  build_id = request.form['build_id'].strip()
  build_web_url = request.form['build_web_url'].strip()
  job_id = request.form['job_id'].strip()
  job_web_url = request.form['build_web_url'].strip()

  time.sleep(10)

  tt_logfile = tempdir + os.sep + build_uuid + '-' + build_id + '-' + job_id + '.log'

  urllib.request.urlretrieve('https://api.travis-ci.com/v3/job/' + job_id + '/log.txt', tt_logfile)

  startup_duration = ''
  with open(tt_logfile, 'r') as ttlog:
    for line in ttlog:
      if line.startswith('startup:'):
        startup_duration = line.split(':')[1].strip()
        break;


  line = '"' + str(now) + '";' \
           + str(build_id) + ';' \
           + str(job_id) + ';' \
           + '"' + str(startup_duration) + '";' \
           + '"' + str(build_web_url) + '";' \
           + '"' + str(job_web_url) + '";' \
           + '\n'

  with open(tempdir + os.sep + build_uuid + '.csv', 'a') as log_file:
    log_file.write(line)

  return line, status.HTTP_200_OK

if __name__ == '__main__':
  app.run(host='0.0.0.0')
