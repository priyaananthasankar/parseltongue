import pytest
import subprocess
import os
import signal
import requests
import json
import time

pro = None

@pytest.fixture
def init_func():
    pass
    #subprocess.Popen("func host start",shell=True)
    # The os.setsid() is passed in the argument preexec_fn so
    # it's run after the fork() and before  exec() to run the shell.
    #pro = subprocess.Popen(['func','host','start'],stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
    #yield
    #print("tearing down functions host...")
    #os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def test_eg_validation(init_func):
    with open('subvalidation.json') as f:
        payload = json.load(f)
        r = requests.post('http://localhost:7071/api/HttpTrigger1', json = payload)
        print(r.status_code,r.json())
        assert 'validationResponse' in str(r.json())
