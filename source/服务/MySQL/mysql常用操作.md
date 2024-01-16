# MySQL常用操作

## 连接mysql
```bash
# 本地
mysql -uroot -p123456

# 远程
mysql -h192.168.1.100 -P3306 -uroot -p123456

# 指定sock
mysql -S /tmp/mysql.sock -uroot -p123456

# 终端执行sql命令
mysql -uroot -p123456 -e "show databases;"
```
> - -u: 用户名
> - -p: 密码
> - -e: 执行sql命令
> - -S: 指定sock
> - -P: 指定端口
> - -h: 指定远程地址

## 创建用户和授权
```mysql
# 创建用户
CREATE USER 'username'@'host' IDENTIFIED BY 'password';

# 授权
GRANT privileges ON databasename.tablename TO 'username'@'host';

# 刷新权限
FLUSH PRIVILEGES;

# 查询权限
SHOW GRANTS FOR 'username'@'host';  # 查看指定用户
SHOW GRANTS;  # 查看当前用户
```
> - `host`: 指定允许使用这个账号登陆的IP地址，%表示所有IP地址。192.168.1.%表示192.168.1网段的所有IP地址。
> - `privileges`: 权限，如SELECT, INSERT, UPDATE等，如果要授予所有权限则使用ALL。
> - `databasename.tablename`: 数据库名和表名，分别用*号表示所有。

## 常用命令
```mysql
# 查询库 
show databases;

# 切换库 
use mysql;

# 查看库里的表
show tables;

# 查看表里的字段 
desc tb_name;

# 查看建表语句 
show create table tb_name\G

# 查看当前用户 
select user();

# 查看当前使用的数据库 
select database();

# 创建库 
create database db1;

# 创建表 
use db1; 
create table t1(`id` int(4), `name` char(40));

# 查看当前数据库版本 
select version();

# 查看数据库状态 
show status;

# 查看各参数 
show variables; 
show variables like 'max_connect%';

# 修改参数 
set global max_connect_errors=1000;

# 查看队列中的进程
select * from information_schema.processlist;
show processlist; 
show full processlist;
```

## 常用sql语句
```mysql
# 查询mysql库下user表有多少行
select count(*) from mysql.user;

# 查询mysql库db表的所有字段
select * from mysql.db;

# 查询db字段的内容
select db from mysql.db;

# 查询多个字段内容
select db,user from mysql.db;

# 查询字段中指定内容，where=条件
select * from mysql.db where host like '192.168.%';
```

## mysqldump备份和恢复
```bash
# 备份某个库
mysqldump -u用户名 -p密码 库名 > /path/文件名.sql

# 备份多个库
mysqldump -u用户名 -p密码 -B 库名1 库名2 库名3 > /path/文件名.sql

# 备份所有库
mysqldump -u用户名 -p密码 -A > /path/文件名.sql

# 恢复库
mysql -u用户名 -p密码 库名 < /path/文件名.sql
```
```bash
# 备份表
mysqldump -u用户名 -p密码 库名 表名 > /path/文件名.sql

# 备份表结构
mysqldump -u用户名 -p密码 -d 库名 表名 > /path/文件名.sql

# 恢复表
mysql -u用户名 -p密码 库名 < /path/文件名.sql
```
