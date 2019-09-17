#!/bin/bash
echo $1  ALL=\(ALL:ALL\) ALL >> /etc/sudoers
mkdir /etc/skel/.ssh
chmod 700 /etc/skel/.ssh
useradd -G admin -m --skel /etc/skel/ $1
echo "$1:$2" | chpasswd
chsh -s /bin/bash $1