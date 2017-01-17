#!/usr/bin/env python

import os
import sys
import json
import re

API_HOST='use.cloudshare.com'

# TODO: Support for --host? (obsolete, since _meta was introduced in 1.3:
#    http://docs.ansible.com/ansible/dev_guide/developing_inventory.html#tuning-the-external-inventory-script

def die(msg):

    print msg
    sys.exit(1)

try:
    import cloudshare
except ImportError:
    die("Unable to find CloudShare Python SDK.\nHave you run 'pip install cloudshare'?")

for envar in ["CLOUDSHARE_API_KEY", "CLOUDSHARE_API_ID"]:
    if envar not in os.environ:
        die("%s must be defined." % envar)

api_key = os.environ["CLOUDSHARE_API_KEY"]
api_id = os.environ["CLOUDSHARE_API_ID"]

def api(path, method='GET'):
    return cloudshare.req(hostname=API_HOST, method=method, path=path, apiId=api_id, apiKey=api_key).content


def get_extended(env_id):
    return api("envs/actions/getextended?envId=%s" % env_id)

def get_ssh_info(env_id):
    return get_extended(env_id)


def safe_name(name):
    return re.sub(r"[ -]+", '-', name).lower()


groups = {}

vm_host_vars = {}

for env in api('envs'):
    id = env['id']
    info = get_ssh_info(id)

    name = safe_name(info['name'])
    extended = get_extended(id)
    vms = [safe_name(vm['name']) for vm in extended['vms'] if vm['fqdn']]
    groups[name] = {
        "hosts": vms
    }
    for vm in extended['vms']:
        if not vm['fqdn']:
            continue

        vm_host_vars[safe_name(vm['name'])] = {
            'ansible_ssh_user': vm['username'],
            'ansible_ssh_pass': vm['password'],
            'ansible_host': vm['fqdn']
        }

groups['_meta'] = { 'hostvars': vm_host_vars }

print json.dumps(groups, indent=2)
