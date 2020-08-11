#!/usr/bin/env python3

import os
import sys
import json

# Google Imports
import googleapiclient.discovery
from google.oauth2 import service_account

# Celery Imports
from celery import Celery
app = Celery()


# Required to use service accounts with the Google Python API Module
def get_client(scopes, service=['admin', 'directory_v1']):
    # When you use a service account you have to specify the subject as the
    # user performing the actions. This wasn't clear when I started and
    # produces an unhelpful error otherwise.
    creds = service_account.Credentials.from_service_account_file(
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=scopes,
        subject=os.environ['GOOGLE_USER'],
    )
    return googleapiclient.discovery.build(service[0], service[1], credentials=creds)


# user is the task body, which is a dict in the form expected by the Python APIs
@app.task(bind=True, rate_limit='10/s', max_retries=3)
def user_create(self, user):
    try:
        client = get_client([
            'https://www.googleapis.com/auth/admin.directory.user',
        ])
        resp = client.users().insert(body=user).execute()
        json.dump(resp, sys.stderr)
        sys.stderr.flush()
    except Exception as exc:
        raise self.retry(exc=exc)
