#!/bin/bash

echo "------------------------- MOUNT"
mount | grep -v -E 'type (ext4|tmpfs|devpts|proc|sysfs|binfmt_misc|rpc_pipefs)'
echo "------------------------- PS"
ps -eo args | grep -v '^\['
echo "------------------------- YUM"
yum list installed

