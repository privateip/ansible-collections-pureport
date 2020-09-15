# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = '''
  callback: pureport.network.cli
  short_description: Handles CLI output to screen for Pureport collections
  description:
    - This callback handles all stdout for the Pureport cloud CLI
  type: stdout
  requirements:
    - Set as stdout in config
  options:
    template_path:
      description: Path to the CLI output templates
      default: ~/.pureport/templates
      env:
        - name: PUREPORT_TEMPLATES_PATH
      type: path
'''


import os

from jinja2 import Environment, FileSystemLoader

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "stdout"
    CALLBACK_NAME = "pureport.network.cli"

    def v2_runner_on_ok(self, result):

        #import q; q.d()

        #if result._task.name:
        #    self._display.display(result._task.name)

        for tag in result._task.tags:
            if tag.startswith('template:'):
                _, template_file = tag.split(':')

                templates_path = self.get_option('template_path')
                env = Environment(trim_blocks=True, lstrip_blocks=True, loader=FileSystemLoader(templates_path))
                template = env.get_template(template_file)

                if result._task.register:
                    variables = {result._task.register: result._result}
                else:
                    variables = {}

                self._display.display(template.render(variables))
