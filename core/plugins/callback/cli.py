# (c) 2020 Pureport
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION =  """
  name: pureport.core.cli
  type: stdout
  author: Pureport
  short_description: Displays output to stdout
  description:
    - Displays the output of plays and tasks
"""

import datetime
import shutil

from ansible.plugins.callback import CallbackBase
from ansible import constants as C
from ansible.utils.color import stringc


def current_time():
    return '%sZ' % datetime.datetime.utcnow().isoformat()


class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "stdout"
    CALLBACK_NAME = "pureport.core.cli"

    def v2_playbook_on_play_start(self, play):
        self._start_time = datetime.datetime.now()
        #self._display.display("run started at {}".format(current_time()))

    def v2_playbook_on_stats(self, stats):
        elapsed_time = datetime.datetime.now() - self._start_time
        #self._display.display("run completed in {}".format(elapsed_time))

    def v2_runner_on_ok(self, result):


        #if result._task.register:
        if result._task.action == 'pureport.core.stdout':

            if result._result.get('changed'):
                status_text = u'[changed]'
                color = C.COLOR_OK
            else:
                status_text = u'[ok]'
                color = C.COLOR_OK

            result_status = stringc(status_text, color)

            #text = result._task.name
            text = result._result['display']

            textlen = len(text) +  len(status_text)
            cols = shutil.get_terminal_size().columns

            text += '.' * (cols - textlen)
            text += result_status


            self._display.display(text)

    #def v2_runner_on_skipped(self, result):
    #    if result._task.register:
    #        result_status = "[skipped]"

    #        textlen = len(result._task.name) +  len(result_status)
    #        cols = shutil.get_terminal_size().columns

    #        text = result._task.name
    #        text += '.' * (cols - textlen)
    #        text += result_status

    #        self._display.display(text, color=C.COLOR_SKIP)


    def v2_runner_on_failed(self, result, ignore_errors=False):
        result_status = "[FAILED]"

        textlen = len(result._task.name) +  len(result_status)
        cols = shutil.get_terminal_size().columns

        text = result._task.name
        text += '.' * (cols - textlen)
        text += result_status

        self._display.display(text)
