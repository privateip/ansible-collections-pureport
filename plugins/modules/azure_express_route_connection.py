#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'Pureport'
}

DOCUMENTATION = '''
---
module: azure_express_route_connection
short_description: Create, update or delete a Azure Express Route connection
description:
    - "Create, update or delete a Azure Express Route connection"
version_added: "2.8"
requirements: [ pureport-client ]
author: Matt Traynham (@mtraynham)
options:
    network_href:
        required: true
    service_key:
        description:
            - The Azure Express Route service key.
        required: true
        type: str
extends_documentation_fragment:
    - pureport.pureport.client
    - pureport.pureport.network
    - pureport.pureport.state
    - pureport.pureport.resolve_existing
    - pureport.pureport.wait_for_server
    - pureport.pureport.connection_args
    - pureport.pureport.peering_connection_args
'''

EXAMPLES = '''
- name: Create a simple PRIVATE Azure Express Route connection for a network
  azure_express_route_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Azure Express Route Connection
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    service_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    wait_for_server: true  # Wait for the server to finish provisioning the connection
  register: result  # Registers the connection as the result

- name: Update the newly created connection with changed properties
  azure_express_route_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: {{ result.name }}
    speed: 100
    high_availability: {{ result.high_availability }}
    location_href: {{ result.location.href }}
    billing_term: {{ result.billing_term }}
    service_key: {{ result.service_key }}
    wait_for_server: true  # Wait for the server to finish updating the connection
  register: result  # Registers the connection as the result

- name: Delete the newly created connection using the 'absent' state
  azure_express_route_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    state: absent
    name: {{ result.name }}
    speed: {{ result.speed }}
    high_availability: {{ result.high_availability }}
    location_href: {{ result.location.href }}
    billing_term: {{ result.billing_term }}
    service_key: {{ result.service_key }}
    wait_for_server: true  # Wait for the server to finish deleting the connection

- name: Create a PRIVATE Azure Express Route connection with all properties configured
  azure_express_route_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Azure Express Route Connection
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    service_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    # Optional properties start here
    description: My Ansible managed Azure Express Route connection
    peering_type: PRIVATE
    customer_networks:
      - address: a.b.c.d/x  # A valid CIDR address
        name: My Azure accessible CIDR address
    nat_enabled: true
    nat_mappings:
      - a.b.c.d/x  # A valid CIDR address, likely referencing a Customer Network

- name: Create a PUBLIC Azure Direct Connect connection with all properties configured
  azure_express_route_connection:
    api_key: XXXXXXXXXXXXX
    api_secret: XXXXXXXXXXXXXXXXX
    network_href: /networks/network-XXXXXXXXXXXXXXXXXXXXXX
    name: My Ansible Azure Express Route Connection
    speed: 50
    high_availability: true
    location_href: /locations/XX-XXX
    billing_term: HOURLY
    service_key: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
    # Optional properties start here
    description: My Ansible managed Azure Express Route connection
    peering_type: PUBLIC
'''

RETURN = '''
connection:
    description: the created, updated, or deleted connection
    type: Connection
'''

from functools import partial
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import \
    camel_dict_to_snake_dict, \
    snake_dict_to_camel_dict

from ..module_utils.pureport import \
    get_client_argument_spec, \
    get_client_mutually_exclusive, \
    get_network_argument_spec
from ..module_utils.pureport_crud import \
    get_state_argument_spec, \
    get_resolve_existing_argument_spec
from ..module_utils.pureport_connection_crud import \
    get_wait_for_server_argument_spec, \
    get_connection_argument_spec, \
    get_cloud_connection_argument_spec, \
    get_peering_connection_argument_spec, \
    connection_crud


def construct_connection(module):
    """
    Construct a Connection from the Ansible module arguments
    :param AnsibleModule module: the Ansible module
    :rtype: Connection
    """
    connection = dict((k, module.params.get(k)) for k in (
        'id',
        'name',
        'description',
        'speed',
        'high_availability',
        'billing_term',
        'customer_networks',
        'service_key'
    ))
    connection.update(dict(
        type='AZURE_EXPRESS_ROUTE',
        peering=dict(type=module.params.get('peering_type')),
        location=dict(href=module.params.get('location_href')),
        nat=dict(
            enabled=module.params.get('nat_enabled'),
            mappings=[dict(native_cidr=nat_mapping)
                      for nat_mapping in module.params.get('nat_mappings')]
        )
    ))
    connection = snake_dict_to_camel_dict(connection)
    return connection


def main():
    argument_spec = dict()
    argument_spec.update(get_client_argument_spec())
    argument_spec.update(get_network_argument_spec(True))
    argument_spec.update(get_state_argument_spec())
    argument_spec.update(get_resolve_existing_argument_spec())
    argument_spec.update(get_wait_for_server_argument_spec())
    argument_spec.update(get_connection_argument_spec())
    argument_spec.update(get_cloud_connection_argument_spec())
    argument_spec.update(get_peering_connection_argument_spec())
    argument_spec.update(
        dict(
            service_key=dict(type='str', required=True)
        )
    )
    mutually_exclusive = []
    mutually_exclusive += get_client_mutually_exclusive()
    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=mutually_exclusive
    )
    # Using partials to fill in the method params
    (
        changed,
        changed_connection,
        argument_connection,
        existing_connection
    ) = connection_crud(
        module,
        partial(construct_connection, module)
    )
    module.exit_json(
        changed=changed,
        **camel_dict_to_snake_dict(changed_connection)
    )


if __name__ == '__main__':
    main()
