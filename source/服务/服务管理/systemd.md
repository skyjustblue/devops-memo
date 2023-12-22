# systemd
centos7以后用于服务管理。  

systemd可以管理正在运行的服务，同时提供比SystemV 多得多的状态信息。它还管理硬件、进程和进程组、文件系统挂载等。

## 用法
### 列出所有服务
```
$ systemctl list-units --type=service
```

### 列出所有已启动的服务
```
$ systemctl list-units --type=service --state=running
```

### 服务状态管理命令
```
# 查看服务状态
$ systemctl status httpd.service

# 启动服务
$ systemctl start httpd.service

# 重启服务
$ systemctl restart httpd.service

# 重新加载服务
$ systemctl reload httpd.service

# 开机自启服务
$ systemctl enable httpd.service

# 查看服务是否开机自启
$ systemctl is-enabled httpd.service

# 关闭服务
$ systemctl stop httpd.service

# 禁止开机自启服务
$ systemctl disable httpd.service
```

### mask参数 - 隐藏服务
服务被隐藏后，无法再对服务进行：`start` `stop` `restart` `reload` 等操作，但仍然可以查看服务状态。

```
# 隐藏服务
$ systemctl mask httpd.service

# 取消隐藏服务
$ systemctl unmask httpd.service
```

### unit
systemd可以管理所有的系统资源，不同的资源统称为unit（单元）

Unit 文件统一了过去各种不同系统资源配置格式，例如服务的启/停、定时任务、设备自动挂载、网络配置、虚拟内存配置等。而 Systemd 通过不同的文件后缀来区分这些配置文件。

#### systemd包括12种文件类型
- service：系统服务
- target：多个unit组成的组
- device：硬件设备
- mount：文件系统挂载点
- automount：自动挂载点
- path：文件或路径
- scope：不是由systemd启动的外部进程
- slice：进程组
- snapshot：systemd快照，可以切回某个快照
- socket：进程间通信的套接字
- swap：us文件
- timer：定时器

unit配置文件存在路径：`/usr/lib/systemd/system/`

#### unit相关命令
```
# 列出所有运行的unit
$ systemctl list-units

# 列出所有，包括失败或者inactive的
$ systemctl list-units --all

# 列出所有inactive的unit
$ systemctl list-units --all --state=inactive

# 列出所有active的unit
$ systemctl list-units --all --type=service

# 查看服务是否active
$ systemctl is-active httpd.service
```

#### target
target是多个unit组成的组。启动一个target就是启动该组内所有的unit，停止一个target就是停止该组内所有的unit。
- 一个service属于一种类型的unit
- 多个unit组成一个target
- 一个target包含多个service（unit）

##### 用法
```
# 查看sshd属于哪个target
$ systemctl list-dependencies sshd.service

# 查看所有target
$ systemctl list-units --type=target

# 查看指定target下unit
$ systemctl list-dependencies multi-user.target

# 查看系统默认target
$ systemctl get-default

# 设置默认target
$ sudo systemctl set-default multi-user.target
```

