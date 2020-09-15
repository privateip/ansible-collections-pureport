# (c) 2020 Pureport
#
# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import hashlib
import json

from ansible.errors import AnsibleError, AnsibleFilterError

def get_hash(data, hashtype='sha1'):

    try:  # see if hash is supported
        h = hashlib.new(hashtype)
    except Exception:
        return None

    if isinstance(data, list):
        data = ':'.join([str(d) for d in data])

    h.update(to_bytes(data, errors='surrogate_or_strict'))
    return h.hexdigest()



class FilterModule(object):
    ''' Ansible core jinja2 filters '''

    def filters(self):
        return {
            'hash': get_hash,
        }
