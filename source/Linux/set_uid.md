# set_uid（u的特殊权限）
setuid（即suid：保存设置用户ID）：当一个可执行文件或程序设置为setuid时，任何一个用户执行这个进程时对应的euid(effective user id)都会被设置为文件所有者的uid。

## 扩展知识ruid和euid
每一个linux进程都会包含这两个uid。
* ruid（实际用户ID）（real user id）：当前使用系统的用户id，在用户登录时由系统设置。
* euid（有效用户ID）（effective user id）：用于系统判断用户对系统资源有哪些权限。用户执行任意操作时，都会由euid进行判断，有则成功，没有则报错。正常情况下，用户登陆系统后，euid和ruid是相同的，但是当用户想要执行某些特殊程序时（如当前ruid无法执行的程序），euid和ruid可以发生变化，这里的变化可以通过suid改变。

## 语法

    $ chmod {u,g,o,a}{+,-,=}s file
    或者
    $ chmod 4775 file

<kbd>4775</kbd>中的<kbd>4</kbd>表示：所属主。
<kbd>2</kbd>：所属组。
<kbd>1</kbd>：其他。


## 实例
### 添加setuid位：

```
有执行权限：
[root@lwz01 ~]# chmod u+s /usr/bin/ls
[root@lwz01 ~]# ll /usr/bin/ls
-rwsr-xr-x. 1 root root 117608 Aug 20  2019 /usr/bin/ls

没有执行权限：
[root@lwz01 ~]# chmod 4664 /usr/bin/passwd 
[root@lwz01 ~]# ll /usr/bin/passwd 
-rwSrw-r--. 1 root root 27832 Jun 10  2014 /usr/bin/passwd
```
> * *当文件有执行权限或者增加了执行权限时，添加的setuid位为小写"s"，即setuid生效，所有用户执行此文件都以拥有者的权限来执行（一般拥有者都是root用户）。*
> * *当文件没有执行权限或者取消了执行权限时，添加的setuid位为大写"S"，即setuid失效，所有人无法执行文件。*

### 取消setuid位：

```
[root@lwz01 ~]# chmod u-s /usr/bin/ls
或者
[root@lwz01 ~]# chmod 0755 /usr/bin/ls
```

### 验证
切换普通用户修改密码：
```
[root@lwz01 ~]# su - lwz
[lwz@lwz01 ~]$ /usr/bin/passwd lwz
-bash: /usr/bin/passwd: Permission denied
```

