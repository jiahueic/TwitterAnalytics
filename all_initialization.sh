#!/bin/bash
ansible-playbook -i hosts.ini couchdbcluster.yml -e 'ansible_python_interpreter=/usr/bin/python3'
ansible-playbook -i hosts.ini couchdbcluster2.yml 'ansible_python_interpreter=/usr/bin/python3'
ansible-playbook  test.yml -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass
ansible-playbook test_withvolume.yml -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass
ansible-playbook -i hosts.ini couchdb.yml 'ansible_python_interpreter=/usr/bin/python3'
ansible-playbook couchdb_twitter.yml --ask-become-pass
ansible-playbook mastadon.yml -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass
ansible-playbook create_twitter_views.yml -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass
ansible-playbook -i hosts.ini mastadon_harverster.yml -e 'ansible_python_interpreter=/usr/bin/python3'
ansible-playbook -i hosts.ini insert_data.yml -e 'ansible_python_interpreter=/usr/bin/python3' --ask-become-pass

