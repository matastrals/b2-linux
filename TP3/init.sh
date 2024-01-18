#!/bin/bash
# -*- ENCODING: UTF-8 -*-
groupadd backup
useradd -m -d /srv/backup -s /usr/bin/nologin backup
usermod -aG backup backup
mkdir /var/log/backup/
chmod 700 /var/log/backup/
chown backup /var/log/backup/ -R backup
chown backup.service
chown backup backup.service
chown backup backup.timer
chmod 700 backup.service
chmod 700 backup.timer
mv backup.service /srv/backup/
mv backup.timer /srv/backup/
systemctl daemon-reload
systemctl start backup.timer
systemctl enable backup.timer
