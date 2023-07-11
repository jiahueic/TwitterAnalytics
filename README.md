# COMP90024 Assignment 2 (Team 22) README
Welcome to the README file of COMP90024 Assignment 2 (Team 22). This document outlines the folder/file structure of our repository on our main branch. 
## Folder/File Structure
**/data-importing**: Contains Python scripts for filtering tweets with geo location field, appending sa3 region field to tweets with geo location field and for importing the entire 60 GB Twitter data into the CouchDB

**Dockerfile**: defines the Docker configurations for deploying the front-end server
/my-ansible-project: Contains Ansible scripts and bash shell scripts which wrap around multiple Ansible scripts

There are various subdirectories in /my-ansible-project:
- **/docker**: This folder contains thev required Docker files to build the Mastodon harvester Docker image and container.
- **/data-importing**: This folder has the same functionality as aforementioned. However, this folder contains some 
additional bash shell scripts which wraps around the Python scripts and these shell scripts are called in the Ansible tasks.
- **/docker_fastapi**: Contains the FastAPI docker files to lauch an image and run the docker container for the back-end server.
- **/docker_vuejs**: Contains the front-end (VueJS) docker files to lauch and image and run the docker container for the front-end server.
- **/mastadon_script**: Contains the Python scripts for running the Mastodon harvesters and bash shell scripts which wrap around them. Also contains Python scripts which creates MapReduce views of Mastodon databases in CouchDB.
- **/twitter_script**: Contains the Python script for creating SA3 and tag count views in Twitter related databases.
- **ansible.md**: Readme file on how to invoke automated system deployment from scratch. 
- **jia.pem** : The private key file to access the MRC Virtual Machines.
- **unimelb-comp90024-2023-grp22-openrc.sh**: Provides the credentials for connecting to the OpenStack API in MRC, the corresponding OpenAPI password is not provided in this repo.
 

 
**Report+Architecture+WebApplication+MRC  Feedback**
There was no need to be able to deploy the whole system through Ansible - it was really only required to show how it could be used to scale the system (not a bad thing that you did this anyway!). Nice that you explored more disaggregated scenarios (SA3 etc). Could you not use 2021 Census data from SUDO? The scenarios were fine, although when I tested the web application it had a few issues, e.g. the blended heatmap had issues and the pop up information windows had no content. (This was a minor thing as it worked in the demo and in the report). It would have been better if you had used an official data dictionary of terms for the processing of tweets, e.g. rather than hardcoding some terms like depression, selfcare etc you might have used a richer and more established source. The architecture was fine and it was good that you used Docker and had a clustered couchDB. There should not have been a need to have two separate couchDB clusters for the Twitter/SUDO and for the Mastodon data though. You could / should have put them into a single couchDB cluster. You used Docker but you might also have tried Docker SWARM for the scaling. The pros and cons of MRC were fine, but I was rather expecting a bit more real world experiences of your using the MRC.

**Software Feedback**
General: a solid effort but with a rather confusing repository structure and poor coding practice.
Repository: the layout is rather confusing and should have had a directory for the frontend rather than having it at root level; some files should not have been committed to the repository (node_modules, private keys, *.pyc); dependencies management (requirements.txt or install script with package versions) seems to be missing; it is rather confusing to find MapReduce views under '/my-ansible-project/docker/mastadon_script'; some files are empty ('Analysis5Views.vue'); more READMEs in subdirectories would have made the content more understandable.
Harvester: the use of hardcoded parameters makes the applications inflexible, and when credentials are hardcoded it becomes a security liability; partial use of argparse in new_harvester.py;
Processing: good use of ijson to parse the big Twitter file;
Database: it seems different CouchDB instances are used instead of a clustered database; the use of argparse would have been good if it had included CouchDB credentials, which are hardcoded instead; the use of built-in reduce function would have made 'mydesigndoc/tag_count_map' faster.
Back-end API: good enough, other than some hardcoded parameters and code leftovers (commented out sections, unused variables).
Front-end: OK.

**Ansible and Dynamic Scaling Feedback**
- **Ansible**
In many tasks, you're using the command module, which is not idempotent. This means that running the playbook multiple times could yield different results. To remedy this, consider using Ansible's built-in modules like file for creating directories, and mount for mounting volumes.
The Docker-related tasks could be improved. For instance, you're stopping and removing containers, and then recreating them. It would be better to make use of Docker's restart_policy parameter in the docker_container module, which automatically manages the container's lifecycle.
Ansible roles would be a great way to organize your tasks and make your playbook modular and reusable. It's good practice to split different functionalities into separate roles.
Duplication of code is something to be avoided, and maintaining a single source of truth is an excellent practice. Using Ansible's git module, you could clone the front-end code directly into the desired directory on the target machines.
Hardcoding sensitive information like usernames, passwords, and keys in your playbook is not a good practice. Consider using Ansible Vault to securely store and use such data.
become: true should be used only when you need elevated permissions. Overusing it could lead to potential security issues. In your case, you're already logging in as a privileged user (ubuntu), so you might not need to use become: true for every task.
It's good practice to include error handling in your playbooks. You can use Ansible's failed_when or ignore_errors statements to manage errors gracefully.

- **Docker**
Consider separating commands into multiple layers to leverage Docker caching. For example, apt-get update and apt-get install should be in separate RUN commands.
The tail -f /dev/null at the end might keep the container running, but it is not a recommended practice.
You've correctly set up a build stage, installed your dependencies, and built your app for production. However, it's better to use a multistage build for a smaller image and to avoid unnecessary development dependencies in the production image.

- **Other**
Consider running your application with a proper production-ready HTTP server like NGINX or serve, rather than http-server.


