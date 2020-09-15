# Copyright (c) 2020 Pureport
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = """
  name: pureport.core.api
  plugin_type: inventory
  author: Pureport
  short_description: Inventory plugin for connecting to Pureport API
  description:
    - This inventory plugin populates the Ansible inventory with a single host
      that is responsible for authenticating and communciating with the
      Pureport API
  options:
    config:
      description: Config file to automatically load
      type: path
      env:
        - name: PUREPORT_CONFIG_FILE
    pureport_account_id:
      description: The Pureport account ID
      env:
        - name: PUREPORT_ACCOUNT_ID
    gcp_project:
      description: The Google Cloud project name
      env:
        - name: GCP_PROJECT
"""

from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.parsing.yaml.loader import AnsibleLoader


class InventoryModule(BaseInventoryPlugin):

    NAME = "pureport.core.api"

    def verify_file(self, host_list):
        return True

    def parse(self, inventory, loader, host_list, cache=True):
        super(InventoryModule, self).parse(inventory, loader, host_list)

        self.inventory.add_host('api')
        self.inventory.set_variable('api', 'ansible_connection', 'local')

        data = AnsibleLoader(DOCUMENTATION).get_single_data()
        options = data['options']

        for key in options:
            self.inventory.set_variable('api', key, self.get_option(key))

