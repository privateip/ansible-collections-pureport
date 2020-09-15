from ansible.module_utils.basic import AnsibleModule


def main():
    """Main entry point for Ansible module execution
    """
    argument_spec = {
        'display': dict()
    }

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    result = {'changed': False, 'display': module.params['display']}

    module.exit_json(**result)

if __name__ == '__main__':
    main()
