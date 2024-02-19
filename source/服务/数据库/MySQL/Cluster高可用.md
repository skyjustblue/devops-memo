# Cluster高可用

## 将已有MGR组复制还原成传统主从   
三台节点都执行如下命令：
```bash
# 关闭mysql服务，并清空原数据目录
sudo systemctl stop mysqld
sudo mv /data/mysql /data/mysql.bak
sudo mkdir -p /data/mysql/log ; sudo chown -R mysql:mysql /data/mysql

# 初始化mysql
/usr/local/mysql/bin/mysqld --console --detadir=/data/mysql --initialize-insecure --user=mysql

# 删除my.cnf配置文件中group replication下的所有参数，修改完为如下
[mysqld]
#基础配置不动
server_id = 152                     # 注意修改
gtid_mode = on
enforce_gtid_consistency = on
binlog_checksum = NONE
log_bin = linyi01-bin               # 注意修改
log_replica_updates = 1
binlog_format = row
sync_source_info = 1
sync_binlog = 1
skip_replica_start = 1
relay-log = linyi01-relay-bin       # 注意修改
binlog_transaction_dependency_tracking = WRITESET   # 删除完后增加这一条。开启事务的依赖追踪

# 启动mysql
sudo systemctl start mysqld

# 设置密码
/usr/local/mysql/bin/mysql -uroot -p
use mysql; ALTER USER 'root'@'localhost' IDENTIFIED BY '123123';
flush privileges;
```
```
# my.cnf配置文件更改
loose-group_replication_single_primary_mode=on                  # 启动单主模式
loose-group_replication_enforce_update_everywhere_checks=off    # 关闭多主模式
```
安装mysql-shell（见下面步骤）

创建用户，要授权grant option（见下面步骤）

在lwz1节点执行如下命令：
```
mysqlsh -linyi -p

dba.createCluster('mycluster', {adoptFromGR: true});

# 查看集群状态
dba.getCluster("mycluster").status();
```

## 搭建前系统准备配置
**三台节点都执行**
```
# 主机名设置
hostnamectl  set-hostname lwz1
hostnamectl  set-hostname lwz2
hostnamectl  set-hostname lwz3

# /etc/hosts配置
192.168.1.152	lwz1
192.168.1.156	lwz2
192.168.1.136	lwz3

# 防火墙和selinux关闭
systemctl stop firewalld
systemctl disable firewalld

setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
```

## [安装mysql服务，从头搭建](https://linyi.readthedocs.io/zh/latest/%E6%9C%8D%E5%8A%A1/%E6%95%B0%E6%8D%AE%E5%BA%93/MySQL/%E5%AE%89%E8%A3%85.html#mysql8-0)
**三台节点配置文件：**
```
[mysql]
port = 3306
socket = /tmp/mysql.sock

# 服务端配置
[mysqld]
user = mysql
port = 3306
basedir = /usr/local/mysql
datadir = /data/mysql
socket = /tmp/mysql.sock
pid-file = /data/mysql/mysqld.pid
log-error = /data/mysql/mysql.err

server_id = 152                     # 其他节点需修改
gtid_mode = on
enforce_gtid_consistency = on
binlog_checksum=NONE
log_bin = linyi01-bin               # 其他节点可修改
log_replica_updates = 1
binlog_format = row
sync_source_info = 1
sync_binlog = 1
skip_replica_start = 1
relay-log = linyi01-relay-bin       # 其他节点可修改
binlog_transaction_dependency_tracking = WRITESET
```
```
# 重启服务
systemctl restart mysqld
```

## 安装mysql-shell
**三台节点都安装**
```bash
# 下载，解压
sudo wget https://dev.mysql.com/get/Downloads/MySQL-Shell/mysql-shell-8.0.36-linux-glibc2.12-x86-64bit.tar.gz
sudo tar zxf mysql-shell-8.0.36-linux-glibc2.12-x86-64bit.tar.gz
ln -s /usr/local/mysql-shell-8.0.36-linux-glibc2.12-x86-64bit /usr/local/mysql-shell

# 环境变量
sudo vim /etc/profile.d/mysql-shell.sh
export PATH=$PATH:/usr/local/mysql-shell/bin

source /etc/profile.d/mysql-shell.sh
```
测试mysql-shell是否可用：
```mysqlsh
# 直接执行
mysqlsh

# 测试连接本地mysql服务
shell.connect('root@localhost')

# CTRL+d退出终端
```

## 创建用户
**三台节点都执行**
```
mysql -uroot -p123123

# 创建用户、授权用户
create user 'linyi'@'192.168.%' identified with mysql_native_password by '123123';
grant all on *.* to 'linyi'@'192.168.%' with grant option;
flush privileges;
```

## mysqlsh检测
**节点一执行**，检测三台节点是否成功
```
mysqlsh
dba.checkInstanceConfiguration('linyi@lwz1:3306');
dba.checkInstanceConfiguration('linyi@lwz2:3306');
dba.checkInstanceConfiguration('linyi@lwz3:3306');

# 状态为ok才行，如下显示
The instance 'lwz1:3306' is valid to be used in an InnoDB cluster.

{
    "status": "ok"
}
```

## 创建集群
**节点一中执行**
```
# 登陆
mysqlsh

 MySQL  JS > shell.connect('linyi@lwz1:3306')

# 创建集群
 MySQL  lwz1:3306 ssl  JS > dba.createCluster('mycluster')
 MySQL  lwz1:3306 ssl  JS > var cluster = dba.getCluster()

# 添加节点
 MySQL  lwz1:3306 ssl  JS > cluster.addInstance('linyi@lwz2:3306')
 MySQL  lwz1:3306 ssl  JS > cluster.addInstance('linyi@lwz3:3306')
# 添加节点时会有个选项，如下选择C
Please select a recovery method [C]lone/[A]bort (default Abort): C
```

执行`var cluster = dba.getCluster()`报错：
```
Dba.getCluster: This function is not available through a session to a standalone instance (metadata exists, instance belongs to that metadata, but GR is not active) (MYSQLSH 51314)

# 重启集群后解决
dba.rebootClusterFromCompleteOutage('mycluster')
```

```
# 查看集群状态，状态ok为正常
 MySQL  lwz1:3306 ssl  JS > dba.getCluster("mycluster").status();
{
    "clusterName": "mycluster",
    "defaultReplicaSet": {
        "name": "default",
        "primary": "lwz1:3306",
        "ssl": "REQUIRED",
        "status": "OK",
        "statusText": "Cluster is ONLINE and can tolerate up to ONE failure.",
        "topology": {
            "lwz1:3306": {
                "address": "lwz1:3306",
                "memberRole": "PRIMARY",
                "mode": "R/W",
                "readReplicas": {},
                "replicationLag": "applier_queue_applied",
                "role": "HA",
                "status": "ONLINE",
                "version": "8.0.36"
            },
            "lwz2:3306": {
                "address": "lwz2:3306",
                "memberRole": "SECONDARY",
                "mode": "R/O",
                "readReplicas": {},
                "replicationLag": "applier_queue_applied",
                "role": "HA",
                "status": "ONLINE",
                "version": "8.0.36"
            },
            "lwz3:3306": {
                "address": "lwz3:3306",
                "memberRole": "SECONDARY",
                "mode": "R/O",
                "readReplicas": {},
                "replicationLag": "applier_queue_applied",
                "role": "HA",
                "status": "ONLINE",
                "version": "8.0.36"
            }
        },
        "topologyMode": "Single-Primary"
    },
    "groupInformationSourceMember": "lwz1:3306"
}
```

## 安装mysql-router
高可用需要再至少两台机器上安装mysql-router。因为mysql-router作为请求路由入口，不能存在单点故障，所以还需要额外增加一个实现高可用的软件，如keepalived。

**在节点一和节点二中执行如下命令**
```
# 下载，解压，创建软链接
cd  /usr/local
sudo wget https://dev.mysql.com/get/Downloads/MySQL-Router/mysql-router-8.0.36-linux-glibc2.12-x86_64.tar.xz
sudo tar Jxf mysql-router-8.0.36-linux-glibc2.12-x86_64.tar.xz
sudo ln -s mysql-router-8.0.36-linux-glibc2.12-x86_64 /usr/local/mysql-router

# 配置环境变量
sudo vim /etc/profile.d/mysql-router.sh
export PATH=$PATH:/usr/local/mysql-shell/bin:/usr/local/mysql-router/bin
# 生效
source /etc/profile.d/mysql-router.sh
```
```
# 生成配置文件
mysqlrouter --user=mysql --bootstrap linyi@lwz1:3306
# 输入密码后，成功显示如下
Please enter MySQL password for linyi:
# Bootstrapping system MySQL Router 8.0.36 (MySQL Community - GPL) instance...

- Creating account(s) (only those that are needed, if any)
- Verifying account (using it to run SQL queries that would be run by Router)
- Storing account in keyring
- Adjusting permissions of generated files
- Creating configuration /usr/local/mysql-router-8.0.36-linux-glibc2.12-x86_64/mysqlrouter.conf

# MySQL Router configured for the InnoDB Cluster 'mycluster'

After this MySQL Router has been started with the generated configuration

    $ /etc/init.d/mysqlrouter restart
or
    $ systemctl start mysqlrouter
or
    $ mysqlrouter -c /usr/local/mysql-router-8.0.36-linux-glibc2.12-x86_64/mysqlrouter.conf

InnoDB Cluster 'mycluster' can be reached by connecting to:

## MySQL Classic protocol

- Read/Write Connections: localhost:6446
- Read/Only Connections:  localhost:6447

## MySQL X protocol

- Read/Write Connections: localhost:6448
- Read/Only Connections:  localhost:6449
```
```
# 生成的配置文件为
cat /usr/local/mysql-router/mysqlrouter.conf

# 如下为其文件内容
# File automatically generated during MySQL Router bootstrap
[DEFAULT]
name=system
user=mysql
keyring_path=/usr/local/mysql-router-8.0.36-linux-glibc2.12-x86_64/var/lib/mysqlrouter/keyring
master_key_path=/usr/local/mysql-router-8.0.36-linux-glibc2.12-x86_64/mysqlrouter.key
connect_timeout=5
read_timeout=30
dynamic_state=/usr/local/mysql-router-8.0.36-linux-glibc2.12-x86_64/bin/../var/lib/mysqlrouter/state.json
client_ssl_cert=/usr/local/mysql-router-8.0.36-linux-glibc2.12-x86_64/var/lib/mysqlrouter/router-cert.pem
client_ssl_key=/usr/local/mysql-router-8.0.36-linux-glibc2.12-x86_64/var/lib/mysqlrouter/router-key.pem
client_ssl_mode=PREFERRED
server_ssl_mode=AS_CLIENT
server_ssl_verify=DISABLED
unknown_config_option=error

[logger]
level=INFO

[metadata_cache:bootstrap]
cluster_type=gr
router_id=1
user=mysql_router1_rd9izqk62w04
metadata_cluster=mycluster
ttl=0.5
auth_cache_ttl=-1
auth_cache_refresh_interval=2
use_gr_notifications=0

[routing:bootstrap_rw]
bind_address=0.0.0.0
bind_port=6446
destinations=metadata-cache://mycluster/?role=PRIMARY
routing_strategy=first-available
protocol=classic

[routing:bootstrap_ro]
bind_address=0.0.0.0
bind_port=6447
destinations=metadata-cache://mycluster/?role=SECONDARY
routing_strategy=round-robin-with-fallback
protocol=classic

[routing:bootstrap_x_rw]
bind_address=0.0.0.0
bind_port=6448
destinations=metadata-cache://mycluster/?role=PRIMARY
routing_strategy=first-available
protocol=x

[routing:bootstrap_x_ro]
bind_address=0.0.0.0
bind_port=6449
destinations=metadata-cache://mycluster/?role=SECONDARY
routing_strategy=round-robin-with-fallback
protocol=x

[http_server]
port=8443
ssl=1
ssl_cert=/usr/local/mysql-router-8.0.36-linux-glibc2.12-x86_64/var/lib/mysqlrouter/router-cert.pem
ssl_key=/usr/local/mysql-router-8.0.36-linux-glibc2.12-x86_64/var/lib/mysqlrouter/router-key.pem

[http_auth_realm:default_auth_realm]
backend=default_auth_backend
method=basic
name=default_realm

[rest_router]
require_realm=default_auth_realm

[rest_api]

[http_auth_backend:default_auth_backend]
backend=metadata_cache

[rest_routing]
require_realm=default_auth_realm

[rest_metadata_cache]
require_realm=default_auth_realm
```
```
# 更改文件权限
sudo chown -R mysql  /usr/local/mysql-router/var

# 定义systemd服务启动脚本
sudo vim /lib/systemd/system/mysqlrouter.service

[Unit]
Description=MYSQL Router
After=network.target
[Install]
WantedBy=multi-user.target
[Service]
User=mysql
TimeoutSec=0
PermissionsStartOnly=true
ExecStart=/usr/local/mysql-router/bin/mysqlrouter  -c /usr/local/mysql-router/mysqlrouter.conf
ExecReload=/bin/kill -HUP -
ExecStop=/bin/kill -QUIT
KillMode=process
LimitNOFILE=65535
Restart=on-failure
RestartSec=10
RestartPreventExitStatus=1
PrivateTmp=false

# 启动服务
sudo systemctl daemon-reload
sudo systemctl start mysqlrouter
sudo systemctl enable mysqlrouter

# 查看服务和端口
ps aux |grep mysqlrouter
netstat -lnp |grep mysqlrouter
```

### 测试mysql-router
```
# 在任意台节点测试。6446为读写端口，后端就是组复制中的primary节点，也就是lwz1
mysql -ulinyi -p -h192.168.1.152 -P6446 -e "select @@hostname"
# 输出结果
+------------+
| @@hostname |
+------------+
| lwz1       |
+------------+

# 6447为只读端口，后端就是组复制中的secondary节点，也就是lwz2和lwz3，它们是轮询的。
mysql -ulinyi -p -h192.168.1.152 -P6447 -e "select @@hostname"
# 输出结果会依次为lwz2和lwz3

# 使用循环测试
for i in `seq 10`; do mysql -ulinyi -p'123123' -h192.168.1.152 -P6447 -NB -e "select @@hostname" 2>/dev/null; done
lwz3
lwz2
lwz3
lwz2
lwz3
lwz2
lwz3
lwz2
lwz3
lwz2
```
## 故障模拟
```
# 停掉lwz1
systemctl stop mysqld

# 此时读写节点为lwz3，lwz2为只读

# 再次启动lwz1后，lwz1变为只读节点，lwz3依然是读写
```