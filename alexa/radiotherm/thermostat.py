#from sshtunnel import SSHTunnelForwarder
import requests
import json
from config import *
import paramiko
import forward
import threading
import time
import logger

log = logger.Logger(__name__)

# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(hostname='...', username='...', password='...')
# stdin, stdout, stderr = ssh.exec_command('python hello.py')
# ssh.close()

"""
See link for documentation:
https://github.com/brannondorsey/radio-thermostat

When set to temp heat 68:
'{"temp":67.50,"tmode":1,"fmode":0,"override":1,"hold":0,"t_heat":68.00,"tstate":1,"fstate":0,"time":{"day":1,"hour":8,"minute":48},"t_type_post":0}'

"""

class ThreadState:
    started = False
    run = True


def start_forward(state, ssh):
    log.debug("thread start")
    forward.forward_tunnel(LOCAL_PORT, THERMOSTAT_IP, 80, ssh.get_transport(), state)
    log.debug("thread finish")

def getTemp():

    log.debug("start getTemp()")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=IP_ADDR, port=PORT, username=UN, password=PW)
    state = ThreadState()
    threading.Thread(target=start_forward, args=(state, ssh)).start()

    # while not state.started:
    #     print(".")
    #     time.sleep(2)

    log.debug("before sleep")
    #time.sleep(10)
    while not state.started:
        time.sleep(.01)

    log.debug("sending request")

    r = requests.get('http://{thermostat_ip}:{thermostat_port}/tstat/temp'.format(thermostat_ip='127.0.0.1',
                                                                                  thermostat_port=LOCAL_PORT))
    #server.stop()
    state.run = False
    ssh.close()
    j = json.loads(r.text)
    return j['temp']


def setTemp(temp):

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=IP_ADDR, port=PORT, username=UN, password=PW)
    state = ThreadState()
    threading.Thread(target=start_forward, args=(state, ssh)).start()

    log.debug("before sleep")
    #time.sleep(10)
    while not state.started:
        time.sleep(.01)

    log.debug("sending request")

    r = requests.get('http://{thermostat_ip}:{thermostat_port}/tstat'.format(thermostat_ip='127.0.0.1',
                                                                        thermostat_port=LOCAL_PORT))
    j = json.loads(r.text)

    if 't_heat' in j.keys():
        r = requests.post('http://{thermostat_ip}:{thermostat_port}/tstat'.format(thermostat_ip='127.0.0.1',
                                                                              thermostat_port=LOCAL_PORT),
                      data=json.dumps({'t_heat': temp}))
    elif 't_cool' in j.keys():
        requests.post('http://{thermostat_ip}:{thermostat_port}/tstat'.format(thermostat_ip='127.0.0.1',
                                                                              thermostat_port=LOCAL_PORT),
                      data=json.dumps({'t_heat': temp}))

    state.run = False
    ssh.close()
