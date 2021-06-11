#!/bin/bash
set -e

user=$1
target_parent_home=$2
target_parent_sub_dirs=$3

mv /home/$1 /home/$1_bk
mkdir -p /home/$1
chown $1:$1 /home/$1
chmod 751 /home/$1
ln -s $target_parent_home/$1 /home/$1

SUB_DIRS="Desktop Documents Downloads Pictures Videos Music"

for i in $SUB_DIRS;do
  rm -rf /home/$user/$i/*
  ln -s $target_parent_sub_dirs/$i /home/$user/$i
done
