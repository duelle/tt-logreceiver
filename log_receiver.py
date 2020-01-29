from flask import Flask, escape, make_response, request, send_file
from flask_api import status
import json
import datetime
import time
import urllib.request


app = Flask(__name__)

@app.route("/build/triggered/", methods=['POST'])
def build_triggered():
  now = datetime.datetime.now()
  build_uuid = request.form['build_uuid'].strip()

  line = str(now) + ";" + "triggered" + '\n'

  with open('/tmp/lr_' + build_uuid + '.log', "a") as log_file:
    log_file.write(str(build_uuid) + '\n')
    log_file.write(line)

  return line, status.HTTP_200_OK


@app.route("/job/started/", methods=['POST'])
def job_started():
  now = datetime.datetime.now()

  build_uuid = request.form['build_uuid'].strip()
  build_id = request.form['build_id'].strip()
  build_web_url = request.form['build_web_url'].strip()

  job_id = request.form['job_id'].strip()
  job_web_url = request.form['build_web_url'].strip()

  line = str(now) + ";" \
           + "started" + ";" \
           + str(build_id) + ";" \
           + str(build_web_url) + ";" \
           + str(job_id) + ";" \
           + str(job_web_url) + ";" \
           + '\n'

  with open('/tmp/lr_' + build_uuid + '.log', "a") as log_file:
    log_file.write(line)

  return line, status.HTTP_200_OK

@app.route("/job/finished/", methods=['POST'])
def job_finished():
  now = datetime.datetime.now()

  build_uuid = request.form['build_uuid'].strip()
  build_id = request.form['build_id'].strip()
  build_web_url = request.form['build_web_url'].strip()

  job_id = request.form['job_id'].strip()
  job_web_url = request.form['build_web_url'].strip()

  line = str(now) + ";" \
           + "finished" + ";" \
           + str(build_id) + ";" \
           + str(build_web_url) + ";" \
           + str(job_id) + ";" \
           + str(job_web_url) + ";" \
           + '\n'

  with open('/tmp/lr_' + build_uuid + '.log', "a") as log_file:
    log_file.write(line)

  time.sleep(30)

  urllib.request.urlretrieve('https://api.travis-ci.com/v3/job/' + job_id + '/log.txt', '/tmp/lr_tr_' + build_uuid + '-' + build_id + '-' + job_id + '.log')

  return line, status.HTTP_200_OK

if __name__ == '__main__':
  app.run(host='0.0.0.0')
