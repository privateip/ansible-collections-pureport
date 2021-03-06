#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: connections_info
short_description: Retrieve a list of connections for a account or network
description:
    - "Retrieve a list of connections for a account or network"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    account_href:
        description:
            - The Pureport Account object.
            - This should be the full 'href' path to the Account ReST object (e.g /accounts/abc).
            - One of 'account_href' or 'network_href' should be supplied for this command, but not both.
    network_href:
        description:
            - The Pureport Network object.
            - This should be the full 'href' path to the Network ReST object (e.g /networks/abc).
            - One of 'account_href' or 'network_href' should be supplied for this command, but not both.
extends_documentation_fragment:
    - pureport.pureport.client
    - pureport.pureport.account
    - pureport.pureport.network
'''

EXAMPLES = '''
- name: List connections for an account
  connections_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    account_href: /accounts/ac-XXXXXXXXXXXXXXXXXXXXXX
  register: result   # Registers result.connections

- name: List connections for a network
  connections_info:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
  register: result   # Registers result.connections

- name: Display all connection hrefs using a json_query filter
  debug:
    var: item
  loop: "{{ result.connections | json_query('[*].href') }}"
'''

RETURN = '''
connections:
    description: a list of Connection (dict) objects
    type: list[Connection]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from traceback import format_exc

try:
    from pureport.exception.api import ClientHttpException
except ImportError:
    ClientHttpException = None
from ..module_utils.pureport import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_client, \
    get_account_argument_spec, \
    get_account, \
    get_network_argument_spec, \
    get_network


def find_connections(module):
    """
    List connections
    :param AnsibleModule module: the ansible module
    """
    client = get_client(module)

    connections = None
    # Retrieve connections from the account
    if module.params.get('account_href') is not None:
        account = get_account(module)
        try:
            connections = client.accounts.connections(account).list()
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())
    # Retrieve connections from the network
    elif module.params.get('network_href') is not None:
        network = get_network(module)
        try:
            connections = client.networks.connections(network).list()
        except ClientHttpException as e:
            module.fail_json(msg=e.response.text, exception=format_exc())
    else:
        module.fail_json(msg='One of account_href or network_href '
                             'arguments should be provided.')

    module.exit_json(connections=[camel_dict_to_snake_dict(connection) for connection in connections])


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_account_argument_spec())
    argument_spec.update(get_network_argument_spec())
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    mutually_exclusive += [
        ['account_href', 'network_href']
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    find_connections(module)


if __name__ == '__main__':
    main()
