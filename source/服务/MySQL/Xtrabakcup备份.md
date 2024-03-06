# Xtrabakcup备份
[Xtrabakcup官网](https://www.percona.com/downloads/Percona-XtraBackup-LATEST/)

## 安装
```bash
# 下载，解压，软链接
sudo wget https://downloads.percona.com/downloads/Percona-XtraBackup-8.0/Percona-XtraBackup-8.0.35-30/binary/tarball/percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17.tar.gz
sudo tar zxf percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17.tar.gz -C /usr/local/
sudo ln -s /usr/local/percona-xtrabackup-8.0.35-30-Linux-x86_64.glibc2.17/bin/xtrabackup/usr/bin/
```

## 全量备份
```
# 创建目录，并备份
mkdir -p /data/backup/20240220
xtrabackup --defaults-file=/etc/my.cnf -uroot -p -S /tmp/mysql.sock --backup --target-dir=/data/backup/20240220

# 故障模拟
systemctl stop mysqld
mv /data/mysql /data/mysql-old

## 恢复
# 应用日志
xtrabackup --prepare --apply-log-only --target-dir=/data/backup/20240220/
# 数据准备
xtrabackup --prepare --target-dir=/data/backup/20240220/
# 恢复
xtrabackup -uroot -p --datadir=/data/mysql --copy-back --target-dir=/data/backup/20240220/
# 修改目录权限
chown -R mysql:mysql /data/mysql
systemctl start mysql
```

## 增量备份
```
mkdir -p /data/backup/20240220-2
mkdir -p /data/backup/20240220-2-incr

# 全量备份
xtrabackup --defaults-file=/etc/my.cnf -uroot -p -S /tmp/mysql.sock --backup --target-dir=/data/backup/20240220-2
# 增量备份
xtrabackup --defaults-file=/etc/my.cnf -uroot -p -S /tmp/mysql.sock --backup --target-dir=/data/backup/20240220-2-incr --incremental-basedir=/data/backup/20240220-2

# 故障模拟
systemctl stop mysqld
mv /data/mysql  /data/mysql_old

## 恢复
# 应用全备日志
xtrabackup --prepare --apply-log-only   --target-dir=/data/backup/20240220-2/
# 应用增量日志
xtrabackup --prepare  --target-dir=/data/backup/20240220-2/ --incremental-dir=/data/backup/20240220-2-incr/
# 数据准备
xtrabackup --prepare --target-dir=/data/backup/20240220-2/
# 恢复
xtrabackup -uroot -p --datadir=/data/mysql --copy-back --target-dir=/data/backup/20240220-2/
# 修改目录权限
chown -R mysql:mysql /data/mysql
systemctl start mysql
```

## 多个增量备份
```
mkdir -p /data/backup/20240220-3/full
mkdir -p /data/backup/20240220-3/incr

# 全量
xtrabackup --defaults-file=/etc/my.cnf -uroot -p -S /tmp/mysql.sock --backup --target-dir=/data/backup/20240220-3/full
# 增量1
xtrabackup --defaults-file=/etc/my.cnf -uroot -p -S /tmp/mysql.sock --backup --target-dir=/data/backup/20240220-3/incr/01 --incremental-basedir=/data/backup/20240220-3/full
# 增量2
xtrabackup --defaults-file=/etc/my.cnf -uroot -p -S /tmp/mysql.sock --backup --target-dir=/data/backup/20240220-3/incr/02 --incremental-basedir=/data/backup/20240220-3/incr/01
# 增量3
xtrabackup --defaults-file=/etc/my.cnf -uroot -p -S /tmp/mysql.sock --backup --target-dir=/data/backup/20240220-3/incr/03 --incremental-basedir=/data/backup/20240220-3/incr/02

# 故障模拟
systemctl stop mysqld
mv /data/mysql  /data/mysql_old

## 恢复
# 应用全备日志
xtrabackup --prepare --apply-log-only   --target-dir=/data/backup/20240220-3/full
# 应用增量1日志
xtrabackup --prepare  --apply-log-only --target-dir=/data/backup/20240220-3/full --incremental-dir=/data/backup/20240220-3/incr/01
# 应用增量2日志
xtrabackup --prepare  --apply-log-only --target-dir=/data/backup/20240220-3/full --incremental-dir=/data/backup/20240220-3/incr/02
# 应用增量3日志，最后一次不需要加--apply-log-only
xtrabackup --prepare  --target-dir=/data/backup/20240220-3/full --incremental-dir=/data/backup/20240220-3/incr/03
# 数据准备
xtrabackup --prepare  --target-dir=/data/backup/20240220-3/full
# 恢复
xtrabackup -uroot -p --datadir=/data/mysql --copy-back --target-dir=/data/backup/20240220-3/full
# 修改权限
chown -R mysql:mysql  /data/mysql
systemctl start mysqld
```
