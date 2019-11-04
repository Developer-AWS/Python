#!/usr/bin/python

from paramiko import SSHClient
import paramiko
import sys
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('xxxxxx',username='xxxxxx',key_filename='/home/xxxx/xxxx.pem')

stdin, stdout, stderr = ssh.exec_command("uptime;sudo ln -sf /usr/share/zoneinfo/America/Fortaleza /etc/localtime")
stdin.flush()
data = stdout.read().splitlines()
for line in data:
    print (line)
ssh.close()
