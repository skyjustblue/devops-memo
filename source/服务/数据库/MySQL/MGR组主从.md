# MGR组复制

## 介绍
- **异步复制：** 主库将binlog发送到从库，从库接收并写入relay log，然后从relay log中读取binlog，应用到自己的数据库中。主库并不管从库是否成功应用了binlog，也不等待从库的反馈。（传统复制的同步方式，不能很好的保证主从数据的一致性）
- **半同步复制：** 主库在提交事务前等待至少一个从库确认接收到事务。如果主库发现至少有N个从库已经确认接收到事务，那么主库就会提交事务。这样保证至少有一个从库同步上数据了，也缩短了延迟时间。虽然在一定程度上保证了数据的一致性，但是也不算是非常完美的方案。

    除了一致性方面的问题，无论是异步复制，还是半同步复制，都有一个缺陷：主库宕机，做不到自动切换，需要额外提供三方组件来切换，运维成本高；

- **组复制：**  
    为了解决前面提到的一致性问题和不能自动切换的问题，MySQL官方在2016年时，基于5.7.17版本，出了一个组复制技术 -- MySQL Group Replication（MGR）。MGR以插件形式提供，基于分布式paxos协议，保证数据一致性。内置故障检测和自动选主功能，只要不是集群中的大多数节点都宕机，就可以继续正常工作。提供单主模式与多主模式，多主模式支持多点写入。

    组复制由多个server成员构成，并且组中的每个server成员可以独立地执行事务。但所有读写(RW)事务只有在冲突检测成功后才会提交。只读(RO)事务不需要在冲突检测，可以立即提交。换句话说，对于任何RW事务，提交操作并不是由始发server单向决定的，而是由组来决定是否提交。准确地说，在始发server上，当事务准备好提交时，该server会广播写入值(已改变的行)和对应的写入集(已更新的行的唯一标识符)。然后会为该事务建立一个全局的顺序。最终，这意味着所有server成员以相同的顺序接收同一组事务。因此，所有server成员以相同的顺序应用相同的更改，以确保组内一致。

    在不同server上并发执行的事务可能存在冲突。根据组复制的冲突检测机制，对两个不同的并发事务的写集合进行检测。如在不同的server成员执行两个更新同一行的并发事务，则会出现冲突。排在最前面的事务可以在所有server成员上提交，第二个事务在源server上回滚，并在组中的其他server上删除。 这就是分布式的先提交当选规则。

    MySQL组复制支持单主模型和多主模型两种工作方式(默认是单主模型)。
    -  单主模型：从复制组中众多个MySQL节点中自动选举一个master节点，只有master节点可以写，其他节点自动设置为read only。当master节点故障时，会自动选举一个新的master节点，选举成功后，它将设置为可写，其他slave将指向这个新的master。
    - 多主模型：复制组中的任何一个节点都可以写，因此没有master和slave的概念，只要突然故障的节点数量不太多，这个多主模型就能继续可用。

    **组复制特点：**
    - 高一致性：基于分布式paxos协议实现组复制，保证数据一致性
    - 高容错性：自动检测机制，只要不是大多数节点都宕机就可以继续工作，内置防脑裂保护机制；
    -  高扩展性：节点的添加与移除会自动更新组成员信息，新节点加入后，自动从其他节点同步增量数据，直到与其他节点数据一致；
    - 高灵活性：提供单主和多主模式。

### 部署MGR的需求：
- innodb存储引擎：数据必须存储在innodb存储引擎内，我们通过设置如下参数来禁用其他存储引擎:
    ```
    disabled_storage_engines="MyISAM,BLACKHOLE,FEDERATED,ARCHIVE,MEMORY"
    ```
- 主键：每张表都必须定义一个主键或者等价的非空的唯一键

- IPv4网络：服务器必须支持IPv4网络

- 网络性能：MGR组中的各个服务器必须相互联通且网络性能要求较高

- binlog日志：必须开启二进制日志文件功能

- Slave Updates Logged：组内中的服务器必须可以记录所有事务的日志

- 二进制日志格式：必须设定二进制日志格式为row
    `binlog-format=row`

- 关闭日志校验:设定 `binlog-checksum=NONE`

- 开启GTID：必须开启GTID功能，用来检测MGR中事务的执行情况。 组复制使用全局事务标识符来精确跟踪已在每个服务器实例上提交了哪些事务，从而能够推断出哪些服务器执行了可能与其他位置已提交的事务发生冲突的事务。

- 复制信息存储库：
必须设定如下参数记录主从库的元数据信息
`master-info-repository=TABLE`
`relay-log-info-repository=TABLE`

- 事务写集提取：
设置如下参数使在记录日志的时候同时记录写集，用来检测冲突。 以便在收集行以将其记录到二进制日志时，服务器也收集写集。写集基于每行的主键，并且是标签的简化且紧凑的视图，该标签唯一地标识已更改的行。然后，该标签用于检测冲突。
`transaction-write-set-extraction=XXHASH64`

- 表名小写：
`lower-case-table-names`  在所有组成员该参数设置相同值，innodb中设置为1，注意不同平台的该值可能不一致

- 多线程应用程序：
我们可以设定一些参数使同步进程并行起来
`slave-parallel-workers=N`
`slave-preserve-commit-order=1`
`slave-parallel-type=LOGICAL_CLOCK`

### MGR的一些限制
- 由于MGR依赖于GTID，所以首先有GTID的一些限制

- Gap Locks：   
MGR推荐使用 `READ COMMITTED` 隔离级别来避免使用`Gap Locks`

- Table Locks and Named Locks： 
MGR的验证过程不考虑`table locks` 和`named locks`

- Replication Event Checksums： 
MGR无法使用复制事件检测

- SERIALIZABLE隔离级别：    
MGR不支持串行化隔离级别

- DDL和DML：    
多主模式下，MGR不支持同时不同服务器上的同一个对象的的DDL和DML

- 级联约束的外键索引：  
多主模式下，MGR不支持级联约束的外键索引

- MySQL Enterprise Audit and MySQL Enterprise Firewall：    
MySQL 5.7.21以前，MySQL Enterprise Audit and MySQL Enterprise Firewall使用的是MyISAM表，所以不支持

- 多主模式下死锁：  
多主模式下，SELECT .. FOR UPDATE语句会引发死锁

- Replication Filters： 
MGR不支持复制过滤

- 组大小：  
MGR最多可以有9个成员

- 事务大小的限制：  
    一个成员的独立事务如果过大可能会导致无法在5s内传输到各个节点，这时可能会踢出该成员
    如果我们不设置单独参数限定大小的话，默认为`slave_max_allowed_packet`参数的大小，默认是1G

    我们可以使用如下方法限定MGR中事务的大小
    如果可以减少你事务的大小
    设定`group_replication_transaction_size_limit`参数，5.7中该参数为0，8.0为143M
    `group_replication_compression_threshold` 设定消息大小进行压缩的大小，默认为1M

## 搭建
节点信息：
- 节点1：lwz1，192.168.1.152，Rocky8.8，MySQL8.0.36
- 节点2：lwz2，192.168.1.156，Rocky8.8，MySQL8.0.36
- 节点3：lwz3，192.168.1.136，Rocky8.0，MySQL8.0.36

三个节点分别执行：  
```
# 修改各自的主机名
sudo hostnamectl set-hostname lwz1
sudo hostnamectl set-hostname lwz2
sudo hostnamectl set-hostname lwz3

# 修改hosts文件，每台加入以下全部内容
sudo vim /etc/hosts

192.168.1.152   lwz1
192.168.1.156   lwz2
192.168.1.136   lwz3

# 关闭防火墙和selinux
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
sudo setenforce 0
```
[安装mysql8.0](https://linyi.readthedocs.io/zh/latest/%E6%9C%8D%E5%8A%A1/%E6%95%B0%E6%8D%AE%E5%BA%93/MySQL/%E5%AE%89%E8%A3%85.html#mysql)

如果已经做了主从，需要先将主从信息删除
```
# slave执行
stop slave;
reset slave all;

# master执行
reset master;
```

### 节点1
```bash
# 配置文件/etc/my.cnf

server_id = 152
gtid_mode = on
enforce_gtid_consistency = on
binlog_checksum=NONE
log_bin = linyi01-bin
log_replica_updates = 1
binlog_format = row
sync_source_info = 1
sync_binlog = 1
skip_replica_start = 1
relay-log = linyi01-relay-bin

#group replication参数
loose-group_replication_group_name="cd8e30f8-52df-4b6d-ab8e-e20c117a8acb"  #组的名字，可自定义，但格式为UUID的格式，可以通过命令cat /proc/sys/kernel/random/uuid获取到,但不能用主机的GTID! 所有节点的这个组名必须保持一致！
loose-group_replication_start_on_boot=off  #off:启动mysql时不自动启动组复制，为了避免每次启动自动引导具有相同名称的第二个组。如果开启，此项需要和group_replication_bootstrap_group参数配合使用，其他节点需要同时开启。建议第一次搭建的时候关闭，稳定后再开启。
loose-group_replication_local_address= "192.168.1.152:24901" #本机IP地址，24901用于接收来自其他组成员的传入连接
loose-group_replication_group_seeds= "192.168.1.152:24901,192.168.1.156:24901,192.168.1.136:24901" # 当前主机成员需要加入组时，Server先访问这些种子成员中的一个，然后它请求重新配置以允许它加入组，需要注意的是，此参数不需要列出所有组成员，只需列出当前节点加入组需要访问的节点即可。
loose-group_replication_bootstrap_group=off # 是否自动引导组。此选项只能在一个节点上开启，通常是首次引导组时(或在整组成员关闭的情况下)，如果多次引导，可能出现脑裂。此项开启时，服务重启后才能自动加入组，建议第一次搭建的时候关闭，MGR稳定后再开启。（单主模式下，一般开启此项的默认为主库）
loose-group_replication_single_primary_mode=off #关闭单主模式的参数。
loose-group_replication_enforce_update_everywhere_checks=on #开启多主模式的参数，如果使用单主模式，此参数应该设置为off，相对的单主模式参数设置为on
loose-group_replication_ip_whitelist="192.168.1.0/24,127.0.0.1/8" # 允许加入组复制的客户机来源的ip白名单
```
```bash
# 重启服务
sudo systemctl restart mysqld
```
```mysql
# 登陆mysql配置
# 关闭binlog
SET SQL_LOG_BIN=0;
# 创建组复制用户
create user 'linyi'@'%'  identified with 'mysql_native_password' by '123123';
# 授权
grant REPLICATION SLAVE on *.* to 'linyi'@'%';
# 刷新
flush privileges;
reset master;
# 开启binlog
SET SQL_LOG_BIN=1;

# 配置组复制并安装插件
CHANGE MASTER TO MASTER_USER='linyi', MASTER_PASSWORD='123123' FOR CHANNEL 'group_replication_recovery';
INSTALL PLUGIN group_replication SONAME 'group_replication.so';
# 查看插件信息，主要是看GROUP REPLICATION相关
SHOW PLUGINS;

# 首次启动组的过程称为引导，使用group_replication_bootstrap_group系统变量来引导组，引导程序只能由一台服务器执行一次，且只能执行一次，这就是group_replication_bootstrap_group参数不保存在配置文件中的原因。假如将该参数保存在配置文件中，则在重启时，server会自动引导具有相同名称的第二个组，这将导致两个不同的组具有相同的名称。因此，为了安全的引导组，下面的操作必须到第一个节点执行：
SET GLOBAL group_replication_bootstrap_group=ON;
START GROUP_REPLICATION;
SET GLOBAL group_replication_bootstrap_group=OFF;

# 在执行组引导及启动组复制后，组已经创建出来了，我们可以使用下面命令查看组信息
SELECT * FROM performance_schema.replication_group_members;
+---------------------------+--------------------------------------+-------------+-------------+--------------+-------------+----------------+----------------------------+
| CHANNEL_NAME              | MEMBER_ID                            | MEMBER_HOST | MEMBER_PORT | MEMBER_STATE | MEMBER_ROLE | MEMBER_VERSION | MEMBER_COMMUNICATION_STACK |
+---------------------------+--------------------------------------+-------------+-------------+--------------+-------------+----------------+----------------------------+
| group_replication_applier | 147e60e8-c0e1-11ee-9965-821116f9c471 | lwz1        |        3306 | ONLINE       | PRIMARY     | 8.0.36         | XCom                       |
+---------------------------+--------------------------------------+-------------+-------------+--------------+-------------+----------------+----------------------------+
```

### 节点2、节点3及节点N
节点3以及节点N同节点2一样配置，注意修改`server_id`和本机ip`loose-group_replication_local_address`，`log_bin`和`relay-log`修不修改无所谓。
```bash
# 配置文件/etc/my.cnf

server_id = 156     # 修改节点id
gtid_mode = on
enforce_gtid_consistency = on
binlog_checksum=NONE
log_bin = linyi02-bin       # 设置binlog文件名
log_replica_updates = 1
binlog_format = row
sync_source_info = 1
sync_binlog = 1
skip_replica_start = 1
relay-log = linyi02-relay-bin       # 设置relaylog文件名

#group replication参数
loose-group_replication_group_name="cd8e30f8-52df-4b6d-ab8e-e20c117a8acb"
loose-group_replication_start_on_boot=off       # 其他节点开启时需要所有节点同时开启
loose-group_replication_local_address= "192.168.1.156:24901" #本机IP地址，24901用于接收来自其他组成员的传入连接
loose-group_replication_group_seeds= "192.168.1.152:24901,192.168.1.156:24901,192.168.1.136:24901"
loose-group_replication_bootstrap_group=off         # 只能一个节点开启
loose-group_replication_single_primary_mode=off     # 单主模式。跟随节点1来设置启动单主模式还是多主模式
loose-group_replication_enforce_update_everywhere_checks=on     # 多主模式
loose-group_replication_ip_whitelist="192.168.1.0/24,127.0.0.1/8"
```
```bash
# 重启
systemctl restart mysqld
```
```mysql
# 登陆mysql配置
mysql -uroot -p

# 关闭binlog
SET SQL_LOG_BIN=0;
# 创建组复制用户
create user 'linyi'@'%'  identified with 'mysql_native_password' by '123123';
# 授权
grant REPLICATION SLAVE on *.* to 'linyi'@'%';
# 刷新
flush privileges;
reset master;
# 开启binlog
SET SQL_LOG_BIN=1;

# 配置组复制并安装插件
CHANGE MASTER TO MASTER_USER='linyi', MASTER_PASSWORD='123123' FOR CHANNEL 'group_replication_recovery';
INSTALL PLUGIN group_replication SONAME 'group_replication.so';
# 查看插件信息，主要是看GROUP REPLICATION相关
SHOW PLUGINS;

# 启动组复制。（单主模式时，此命令手动加入组）
START GROUP_REPLICATION;

# 查看组成员，有两个了
SELECT * FROM performance_schema.replication_group_members;
```
