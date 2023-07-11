#!/bin/bash
ansible-playbook -i hosts.ini deploy_server.yml -e 'ansible_python_interpreter=/usr/bin/python3
' --ask-become-pass
ansible-playbook -i hosts.ini deploy_frontend2.yml -e 'ansible_python_interpreter=/usr/bin/python3
' --ask-become-pass
