#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright: (c) 2019, Kazuya Takei <attakei@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community',
}

DOCUMENTATION = '''
---
module: amazon_linux_extras

short_description: Manage topics of amazon-linux-extras

version_added: "2.8"

description:
  - "Manage topics of amazon-linux-extras"
  - "This do not manage package itself"

options:
  name:
    description:
      - Topic name
    required: true
  state:
    description:
      - Set "present" To enable, and set "absent" to disable
    required: true
    choices: [ "absent", "present" ]
    default: "present"
'''

EXAMPLES = '''
# Enable "vim" topic
- name: Enable vim
  ansible_linux_extras:
    name: vim
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', required=True, default='present'),
    )

    result = dict(
        changed=False,
        original_message='',
        message='',
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    if module.check_mode:
        module.exit_json(**result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
