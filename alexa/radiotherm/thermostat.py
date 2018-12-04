from sshtunnel import SSHTunnelForwarder
import requests
import json
from config import *

"""
See link for documentation:
https://github.com/brannondorsey/radio-thermostat

When set to temp heat 68:
'{"temp":67.50,"tmode":1,"fmode":0,"override":1,"hold":0,"t_heat":68.00,"tstate":1,"fstate":0,"time":{"day":1,"hour":8,"minute":48},"t_type_post":0}'

"""

def getTemp():

    server = SSHTunnelForwarder((IP_ADDR, PORT), ssh_username=UN, ssh_password=PW, remote_bind_address=(THERMOSTAT_IP, 80))
    server.start()
    #print(server.local_bind_port)
    r = requests.get('http://{thermostat_ip}:{thermostat_port}/tstat/temp'.format(thermostat_ip='127.0.0.1',
                                                                                  thermostat_port=server.local_bind_port))
    server.stop()
    j = json.loads(r.text)
    return j['temp']


def setTemp(temp):

    server = SSHTunnelForwarder((IP_ADDR, PORT), ssh_username=UN, ssh_password=PW, remote_bind_address=(THERMOSTAT_IP, 80))
    server.start()
    r = requests.get('http://{thermostat_ip}:{thermostat_port}/tstat'.format(thermostat_ip='127.0.0.1',
                                                                                  thermostat_port=server.local_bind_port))
    j = json.loads(r.text)

    if 't_heat' in j.keys():
        r = requests.post('http://{thermostat_ip}:{thermostat_port}/tstat'.format(thermostat_ip='127.0.0.1',
                                                                              thermostat_port=server.local_bind_port),
                      data=json.dumps({'t_heat': temp}))
    elif 't_cool' in j.keys():
        requests.post('http://{thermostat_ip}:{thermostat_port}/tstat'.format(thermostat_ip='127.0.0.1',
                                                                              thermostat_port=server.local_bind_port),
                      data=json.dumps({'t_heat': temp}))

    server.stop()
