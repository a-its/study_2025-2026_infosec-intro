#!/bin/bash
set -e
export LC_ALL=C
source /root/lab06-state/state.env
source /root/lab06-state/functions.sh
systemctl stop httpd
cp -a /root/lab06-state/httpd.conf.before /etc/httpd/conf/httpd.conf
if [ -f /root/lab06-state/port81-changed ]; then
    local_type=$(semanage port -l -C | lab06_port81_type)
    if [ -n "$local_type" ]; then
        semanage port -d -p tcp 81
    fi
fi
if [ -f /root/lab06-state/dontaudit-disabled ]; then
    semodule -B
    command rm /root/lab06-state/dontaudit-disabled
fi
if [ -f /root/lab06-state/test-created ]; then
    command rm -f /var/www/html/test.html
fi
httpd -t
if [ "$lab06_httpd_before" = active ]; then
    systemctl start httpd
else
    if systemctl is-failed --quiet httpd; then
        systemctl reset-failed httpd
    fi
fi
case "$lab06_mode_before" in
    Enforcing) setenforce 1 ;;
    Permissive) setenforce 0 ;;
    *) echo 'STOP: invalid saved SELinux mode'; exit 1 ;;
esac
echo 'RESTORED: Apache config, TCP 81, test file, SELinux mode'
