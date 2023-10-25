# Utility functions for running gRPC HotelReservation in tandem with the Intel IPU emulator

import re
import subprocess
import os


scp_str = 'scp {0} {1}@{2}:{3}'
scp_r_str = 'scp -r {0} {1}@{2}:{3}'
ssh_str = 'ssh {0}@{1}'
unzip_str = 'yes | unzip {0}'
cp_str = 'cp -R {0} {1}'
cd_str = 'cd {0}'
label_add_str = 'sudo docker node update --label-add {0} {1}'


# Validates that ip_address string is in a valid format
def validate_ip(ip_address):
    return re.match(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', ip_address)


def extract_ssh_addr(ssh_line):
    full_login = ssh_line.split()[-1]
    return full_login.split('@')[-1]


def extract_path_end(path):
    return path.split('/')[-1]


def get_node_ssh_list_file(node_ssh_list):
    curr_dir = os.getcwd()
    node_ssh_list_path = curr_dir + '/../node-ssh-lists/' + node_ssh_list
    if not os.path.isfile(node_ssh_list_path):
        ValueError('specified ssh info file does not exist in grpc-hotel-ipu/ssh-node-lists')
    return open(node_ssh_list_path)


# parses output of 'ifconfig -a'
def parse_ifconfig():
    ifconfig_proc = subprocess.Popen(['ifconfig', '-a'],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
    ifconfig_text = ifconfig_proc.communicate()[0].decode('utf-8')

    # TODO: Not sure if every docker manager ip will follow 10.10.1.X format, hardcoded for now
    manager_ip_regex = r'10\.10\.1\.[0-9]{1,3}'
    valid_ips = []
    for line in ifconfig_text.splitlines():
        words = line.split()
        prev_word = ''
        for word in words:
            if (prev_word == 'inet' and
                re.match(manager_ip_regex, word)):
                valid_ips.append(word)
            prev_word = word

    if len(valid_ips) != 1:
        raise ValueError('ifconfig parsing error: none or multiple valid docker manager addresses found')
    return valid_ips[0]


# parses output of 'sudo docker swarm join-token worker'
def parse_swarm_join_token_worker():
    join_token_worker_proc = subprocess.Popen(['sudo', 'docker', 'swarm', 'join-token', 'worker'],
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT)
    join_token_worker_text = join_token_worker_proc.communicate()[0].decode('utf-8')
    join_cmd = ''
    for line in join_token_worker_text.splitlines():
        if 'docker swarm join' in line:
            join_cmd = 'sudo ' + line.strip()
    if join_cmd == '':
        raise ValueError('no valid docker join command found')
    return join_cmd


# parses output of 'sudo docker node ls'
def parse_node_ls():
    node_ls_proc = subprocess.Popen(['sudo', 'docker', 'node', 'ls'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
    node_ls_text = node_ls_proc.communicate()[0].decode('utf-8')
    node_ids = [line.split()[0] for line in node_ls_text.splitlines()[1:]]
    return node_ids
