# set_gid - g的特殊权限
set_gid可以用在文件和目录上，它允许文件或目录的属组被修改。
* 文件：类似于set_uid，普通用户执行的时候临时拥有属组group的权限。
* 目录：任何用户在这个目录下创建的文件或目录的属组都会与set_gid的目录的属组相同。

## 语法

增加：

    $ chmod g+s file

删除：

    $ chmod g-s file

## 实例

### 对目录操作：
```
[root@lwz01 lwz]# chmod g+s 1
[root@lwz01 lwz]# ll
total 0
drwxrwsr-x 3 root lwz  14 Aug 14 11:07 1

[root@lwz01 lwz]# mkdir 1/2
[root@lwz01 lwz]# touch 1/3.txt
[root@lwz01 lwz]# ll 1/
total 0
drwxr-xr-x 2 root root 6 Aug 14 11:07 1
drwxrwsr-x 2 root lwz  6 Aug 24 14:08 2
-rw-rw-r-- 1 root lwz  0 Aug 24 14:08 3.txt
```

### 对文件操作：
当前ls命令没有添加gid权限，所以普通用户无法执行
```
[root@lwz01 lwz]# ll /usr/bin/ls
-rwxr-xr-x. 1 root root 117608 Aug 20  2019 /usr/bin/ls
[root@lwz01 lwz]# su - lwz
Last login: Thu Aug 24 14:00:34 CST 2023 on pts/0
[lwz@lwz01 ~]$ ls /root
ls: cannot open directory /root: Permission denied
```
加上gid权限后，普通用户可以执行ls命令
```
[root@lwz01 lwz]# chmod g+s /usr/bin/ls
[root@lwz01 lwz]# ll /usr/bin/ls
-rwxr-sr-x. 1 root root 117608 Aug 20  2019 /usr/bin/ls
[root@lwz01 lwz]# su - lwz
[lwz@lwz01 ~]$ ls /root
1                error.log              openssl-3.0.1.tar.gz  test1                z1.com
```
