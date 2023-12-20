# firewalld
## 简介

firewall 模块是 firewalld 服务提供的一个用于管理防火墙的模块，它提供了非常丰富的防火墙管理功能，包括端口、服务、接口、区域等。
## 安装

```bash
yum install firewalld -y
```
## 启动关闭服务

```bash
# 启动|关闭|重启服务
systemctl start|stop|restart firewalld

# 开机启动|禁用
systemctl enable|disable firewalld
```

## 基本命令
```
# 查看防火墙状态
$ firewall-cmd --state

# 查看防火墙管理的设备
$ firewall-cmd --get-active-zones

# 查看防火墙生效的区域
$ firewall-cmd --get-default-zone

# 查看防火墙所有区域
$ firewall-cmd --get-zones

# 列出关于public区域的服务设置
$ firewall-cmd --list-all --zone=public

# 列出可使用的服务
$ firewall-cmd --get-services

# 修改默认区域为trusted
$ firewall-cmd --set-default-zone=trusted

# 列出所有打开的端口
$ firewall-cmd --zone=public --list-ports

# 列出所有的域
$ firewall-cmd --list-all-zones
```

## 规则配置

### 查看规则
```
$ firewall-cmd --list-all
```

### 刷新规则
```
$ firewall-cmd --reload
```

### 添加规则
firewall开启后默认是拒绝所有。


#### 开放3306端口
```
$ firewall-cmd --add-port=3306/tcp --permanent
```

#### 开放192.168.1.0/24段所有地址
```
$ firewall-cmd --permanent --add-source=192.168.1.0/24
```

#### 开放http服务
```
$ firewall-cmd --permanent --add-service=http
```

#### 允许192.168.1.110访问80端口
```
$ firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.110" port protocol="tcp" port="80" accept'
```
> `family`指定协议
> `source`指定源地址
> `port`指定端口

### 删除规则

#### 移除3306端口
```
$ firewall-cmd --remove-port=3306/tcp --permanent
```

#### 移除192.168.1.0/24段所有地址
```
$ firewall-cmd --permanent --remove-source=192.168.1.0/24
```

#### 移除http服务
```
$ firewall-cmd --permanent --remove-service=http
```

#### 移除192.168.1.110访问80端口
```
$ firewall-cmd --permanent --remove-rich-rule='rule family="ipv4" source address="192.168.1.110" port protocol="tcp" port="80" accept'
```

#### 拒绝192.168.1.110访问80端口
```
$ firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.110" port protocol="tcp" port="80" reject'
```
> 注意：拒绝及允许同时存在时，效果为拒绝，firewalld中没有先后顺序匹配。

#### 删除所有规则
```
$ firewall-cmd --permanent --remove-all
```

## 端口转发
开启转发功能：
```
$ vi /etc/sysctl.conf
net.ipv4.ip_forward = 1         # 配置文件最下面添加
$ sysctl -p

或者
$ echo 1 > /proc/sys/net/ipv4/ip_forward
```

将访问192.168.1.123(本机)主机8080端口的请求转发至80端口
```bash
# 添加端口转发
$ firewall-cmd --permanent --zone=public --add-forward-port=port=8080:proto=tcp:toport=80:toaddr=192.168.1.123

# 删除端口转发
$ firewall-cmd --permanent --zone=public --remove-forward-port=port=8080:proto=tcp:toport=80:toaddr=192.168.1.123
```

将访问192.168.1.123（本机）主机8080端口的请求转发至192.168.1.111的80端口
```
$ firewall-cmd --permanent --zone=public --add-forward-port=port=8080:proto=tcp:toaddr=192.168.1.111:toport=80
```
> 注意：转发时，要开启伪装，伪装就是SNAT

允许IP伪装：
```
$ firewall-cmd --permanent --zone=public --add-masquerade

$ firewall-cmd --reload

$ firewall-cmd --query-masquerade
```

