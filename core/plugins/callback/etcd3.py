#!/usr/bin/python
#

from __future__ import absolute_import, division, print_function
__metaclass__ = type


import os
import json
import datetime
import traceback

from functools import partial

import etcd3

from ansible.inventory.host import Host
from ansible.parsing.ajson import AnsibleJSONEncoder
from ansible.plugins.callback import CallbackBase


def current_time():
    return '%sZ' % datetime.datetime.utcnow().isoformat()


class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "aggregate"
    CALLBACK_NAME = "pureport.core.etcd3"

    def __init__(self, display=None):
        super(CallbackModule, self).__init__(display)
        self.results = []
        self.registers = {}
        self.client = etcd3.client(host="192.168.1.16")

    def _new_play(self, play):
        return {
            'play': {
                'name': play.get_name(),
                'id': str(play._uuid),
                'duration': {
                    'start': current_time()
                }
            },
            'tasks': []
        }

    def _new_task(self, task):
        return {
            'task': {
                'name': task.get_name(),
                'id': str(task._uuid),
                'duration': {
                    'start': current_time()
                }
            }
        }

    def v2_playbook_on_play_start(self, play):
        self.results.append(self._new_play(play))

    def v2_playbook_on_task_start(self, task, is_conditional):
        if task.register:
            self.results[-1]['tasks'].append(self._new_task(task))

    def _convert_host_to_name(self, key):
        if isinstance(key, (Host,)):
            return key.get_name()
        return key

    def v2_playbook_on_stats(self, stats):
        """Display info about playbook statistics"""

        output = {
            'plays': self.results,
        }

        self.client.put("/test", json.dumps(output, cls=AnsibleJSONEncoder))

    def _record_task_result(self, on_info, result, **kwargs):
        """This function is used as a partial to add failed/skipped info in a single method"""

        host = result._host
        task = result._task

        if host.name != 'api':
            raise AnsibleError("invalid host")

        if task.register:
            task_result = result._result.copy()
            task_result.update(on_info)
            task_result['action'] = task.action
            self.results[-1]['tasks'][-1][host.name] = task_result

            end_time = current_time()

            self.results[-1]['tasks'][-1]['task']['duration']['end'] = end_time
            self.results[-1]['play']['duration']['end'] = end_time

            self.registers[task.register] = self.results[-1]

    def __getattribute__(self, name):
        """Return ``_record_task_result`` partial with a dict containing skipped/failed if necessary"""
        if name not in ('v2_runner_on_ok', 'v2_runner_on_failed', 'v2_runner_on_unreachable', 'v2_runner_on_skipped'):
            return object.__getattribute__(self, name)

        on = name.rsplit('_', 1)[1]

        on_info = {}
        if on in ('failed', 'skipped'):
            on_info[on] = True

        return partial(self._record_task_result, on_info)
