# sudo
## 什么是sudu
`sudo`是linux下的一种权限管理机制，用于用户以其他身份来执行命令，预设的身份为root。

在`/etc/sudoers`中设置了可执行`sudo`指令的用户。若其它未经授权的用户企图使用`sudo`，则会发出警告的邮件给管理员。用户使用`sudo`时，会提示输入密码，而此密码为该用户的口令，而不是root密码。每次输入密码有5分钟的有效期。

## sudo配置文件
`/etc/sudoers`是sudo的配置文件，可以设置哪些用户能够以什么身份执行什么命令。

### visudo命令
`visudo`命令可以用来编辑`/etc/sudoers`文件，保存时会自动检查是否有语法错误。
    
    [root@lwz ~]# visudo    #打开sudoers文件

### sudoers文件配置说明
配置格式：`用户名   ALL=(ALL)   [NOPASSWD:] conmmand`

* `sudoers`文件中的配置项说明：
    * `用户名`：允许使用sudo的用户，多个用户以逗号分隔，或者将多个用户名组成一个别名。
    * `ALL=(ALL)`：其中等号左边的`ALL`表示主机ip或者主机名，一般都为`ALL`。等号右边的`ALL`为左边的用户将授予哪个用户的权限，`ALL`表示所有用户。
    * `NOPASSWD`：表示不需要密码。
    * `command`：表示允许用户执行的命令，命令必须以绝对路径表示。多个命令用逗号隔开。`ALL`表示所有命令。还可以配置命令组别名。

### 实例
#### 用户别名配置
多个用户组成一个别名，方便一次性配置大量用户
```
[root@lwz ~]# visudo
## User Aliases
## These aren't often necessary, as you can use regular groups
## (ie, from files, LDAP, NIS, etc) in this file - just use %groupname
## rather than USERALIAS
# User_Alias ADMINS = jsmith, mikem
User_Alias lin = lwz1,lwz2,lwz3
```

#### 命令组别名配置
先创建命令组别名
```
[root@lwz ~]# visudo
## Command Aliases
## These are groups of related commands...
Cmnd_Alias      CMDS = /bin/ls,/bin/cat,/bin/touch
```
再将命令组别名配置给用户使用
```
## Same thing without a password
# %wheel        ALL=(ALL)       NOPASSWD: ALL
lwz,lwz1     ALL=(ALL)       NOPASSWD:    CMDS
```

## 限制root远程登陆
生产环境中，为了安全起见，应该禁止root用户远程登陆，如果有需求用到root权限，可以通过visudo给普通用户授权。

编辑`/etc/ssh/sshd_config`配置文件禁止root远程登陆：
```
[root@lwz ~]# vi /etc/ssh/sshd_config
#PermitRootLogin yes
PermitRootLogin no

# 重启sshd服务
[root@lwz ~]# systemctl restart sshd
```

root被限制远程登陆后，可以先远程登陆普通用户，再`su - root`切换到root。

取消普通用户登陆root需要密码
```
[root@lwz ~]# visudo
## Same thing without a password
# %wheel        ALL=(ALL)       NOPASSWD: ALL
#lwz,lwz1     ALL=(ALL)       NOPASSWD:    CMDS
lwz     ALL=(ALL)       NOPASSWD: /usr/bin/su - root
```
```
[lwz@lwz ~]$ sudo su - root
上一次登录：五 9月  8 18:24:56 CST 2023pts/0 上
[root@lwz ~]# 
```
