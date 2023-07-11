#!/bin/bash
. unimelb-comp90024-2023-grp-22-openrc.sh
ansible-playbook create_volume.yml
ansible-playbook create_security_group.yml
ansible_playbook create_twitterinstance.yml
ansible_playbook create_couchdbinstance.yml






