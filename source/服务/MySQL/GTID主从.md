# GTID复制

## 介绍
GTID（Global Transaction ID）是MySQL 5.6版本引入的新特性，它是一种基于全局事务ID的复制方式。GTID复制可以解决传统复制中的一些问题，例如主从复制位置错乱、主从库数据不一致等。

事务：
- 事务是数据库执行过程中的一个逻辑工作单位，由一组SQL语句组成，这些SQL语句要么都执行，要么都不执行。
    - 例如，在人员管理系统中，你删除一个人员，你既需要删除人员的基本资料，也要删除和该人员相关的信息，如信箱，文章等等，这样，这些数据库操作语句就构成一个事务！
- 在数据库中，只有使用了Innodb数据库引擎的数据库或表才支持事务。
- 事务具有ACID（原子性、一致性、隔离性、持久性）特性。
    - 原子性：事务是不可分割的工作单位，要么一起完成，要么一起失败。事务在执行过程中发生错误，会被回滚（Rollback）到事务开始前的状态。
    - 一致性：事务完成时，必须使所有的数据都保持一致状态。
    - 隔离性：数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。事务隔离分为不同级别，包括读未提交（Read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（Serializable）。
    - 持久性：事务完成后，对数据的修改就是永久的，即便系统故障也不会丢失。


GTID复制的工作原理：
1. master更新数据时，会在事务前产生GTID，一同记录到binlog日志中。
2. slave端的i/o线程将变更的binlog，写入到本地的relay log中。
3. sql线程从relay log中获取GTID，然后对比slave端的binlog是否有记录。
4. 如果有记录，说明该GTID的事务已经执行，slave会忽略。
5. 如果没有记录，说明该GTID的事务没有执行，slave会执行该GTID的事务，并记录到binlog。
6. 在解析过程中会判断是否有主键，如果有就用二级索引，如果没有就用全部扫描。

GTID比传统复制的优势：
- 无需记录binlog位置和文件名，只需记录GTID，方便管理。
- GTID是全局唯一，不会出现传统复制中主从复制位置错乱的情况。
- GTID是连续没有空洞的，因此主从库出现数据冲突时（主从断开），可以用添加空事物的方式进行跳过，后续再找到事务进行手动恢复。
- 支持在主库上执行DML操作，然后立即在从库上执行相同的操作，保证数据一致性。

## 搭建

先取消传统复制配置
```
# slave执行
stop slave;
reset slave all;

# master执行
reset master;
```

### master配置

(192.168.1.152)master配置：
```
# 修改配置文件my.cnf，重启服务
sudo vim /etc/my.cnf

server_id = 1                 # 设置server_id
log_bin = linyi               # 开启binlog
expire_logs_days = 30         # 清理超过30天的binlog日志
#gtid_mode = on                # 开启gtid。mariadb10.0.2以上默认开启了GTID，这条可以不写
#enforce_gtid_consistency = on # 开启gtid一致性，mariadb10.0.2以上不写这条
binlog_format = row           # 设置binlog格式为row
log-slave-updates = 1         # 开启slave复制，关闭为0
skip-slave-start = 1          # 关闭slave跟随mysql启动而启动

sudo systemctl restart mysqld

# 创建slave授权用户
CREATE USER 'linyi'@'192.168.1.136' IDENTIFIED WITH mysql_native_password BY '123123';
GRANT REPLICATION SLAVE ON *.* TO 'linyi'@'192.168.1.136';
flush privileges;

# 查看master中的binlog信息
show master status;
+--------------+----------+--------------+------------------+
| File         | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+--------------+----------+--------------+------------------+
| linyi.000003 |      324 |              |                  |
+--------------+----------+--------------+------------------+

# 查看master中的GTID
SELECT @@global.gtid_binlog_pos;
+--------------------------+
| @@global.gtid_binlog_pos |
+--------------------------+
| 0-1-1                    |
+--------------------------+

# 通过binlog查看GTID
SELECT BINLOG_GTID_POS('linyi.000003',324);

```

### slave配置
(192.168.1.136)slave配置：
```
# 修改配置文件my.cnf，重启服务
sudo vim my.cnf

server_id = 2                       # 设置server_id，不能和master重复，且不能为0，一般设置为IP最后一段
log_bin = linyi
expire_logs_days = 30
#gtid_mode = on                     # mariadb10.0.2以上不写
#enforce_gtid_consistency = on      # mariadb10.0.2以上不写 
binlog_format = row
log-slave-updates = 1
skip-slave-start = 1

# 重启
sudo systemctl restart mysqld
```

mariadb配置GTID主从
```
stop slave;
# 设置master的GTID
set global gtid_slave_pos='0-1-1';
# 与master建立连接
change master to master_host = '192.168.1.152',master_user = 'linyi',master_password = '123123',master_use_gtid =slave_pos;
# 启动
start slave;

# 查看主从复制状态
MariaDB [(none)]> show slave status\G;
*************************** 1. row ***************************
                Slave_IO_State: Waiting for master to send event
                   Master_Host: 192.168.1.152
                   Master_User: linyi
                   Master_Port: 3306
                 Connect_Retry: 60
               Master_Log_File: linyi.000004
           Read_Master_Log_Pos: 338
                Relay_Log_File: lwz3-relay-bin.000002
                 Relay_Log_Pos: 633
         Relay_Master_Log_File: linyi.000004
              Slave_IO_Running: Yes
             Slave_SQL_Running: Yes
          Replicate_Rewrite_DB:
               Replicate_Do_DB:
           Replicate_Ignore_DB:
            Replicate_Do_Table:
        Replicate_Ignore_Table:
       Replicate_Wild_Do_Table:
   Replicate_Wild_Ignore_Table:
                    Last_Errno: 0
                    Last_Error:
                  Skip_Counter: 0
           Exec_Master_Log_Pos: 338
               Relay_Log_Space: 941
               Until_Condition: None
                Until_Log_File:
                 Until_Log_Pos: 0
            Master_SSL_Allowed: No
            Master_SSL_CA_File:
            Master_SSL_CA_Path:
               Master_SSL_Cert:
             Master_SSL_Cipher:
                Master_SSL_Key:
         Seconds_Behind_Master: 0
 Master_SSL_Verify_Server_Cert: No
                 Last_IO_Errno: 0
                 Last_IO_Error:
                Last_SQL_Errno: 0
                Last_SQL_Error:
   Replicate_Ignore_Server_Ids:
              Master_Server_Id: 1
                Master_SSL_Crl:
            Master_SSL_Crlpath:
                    Using_Gtid: Slave_Pos
                   Gtid_IO_Pos: 0-1-1
       Replicate_Do_Domain_Ids:
   Replicate_Ignore_Domain_Ids:
                 Parallel_Mode: optimistic
                     SQL_Delay: 0
           SQL_Remaining_Delay: NULL
       Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
              Slave_DDL_Groups: 0
Slave_Non_Transactional_Groups: 0
    Slave_Transactional_Groups: 0
```

mysql配置GTID主从
```
stop slave;
change master to master_host='192.168.1.152',master_user='linyi',master_password='123123',master_auto_position=1,master_connect_retry=10;
start slave;

# 查看主从复制状态
show slave status\G;
```