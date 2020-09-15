# Copyright (c) 2020 Pureport
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

from ansible.plugins.inventory import BaseInventoryPlugin


class InventoryModule(BaseInventoryPlugin):

    NAME = "api"

    def verify_file(self, host_list):
        return True

    def parse(self, inventory, loader, host_list, cache=True):
        super(InventoryModule, self).parse(inventory, loader, host_list)
        self.inventory.add_host('api')
        self.inventory.set_variable('api', 'ansible_connection', 'local')
