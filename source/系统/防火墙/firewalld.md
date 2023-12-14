# firewalld
## 简介

firewall 模块是 firewalld 服务提供的一个用于管理防火墙的模块，它提供了非常丰富的防火墙管理功能，包括端口、服务、接口、区域等。
## 安装

```bash
yum install firewalld -y
```
## 基本使用

```bash
# 启动|关闭|重启服务
systemctl start|stop|restart firewalld

# 开机启动|禁用
systemctl enable|disable firewalld
```

## 规则配置

查看规则
```
$ firewall-cmd --list-all
```

允许ip192.168.1.2访问80端口
```bash
$ firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.2" port protocol="tcp" port="80" accept'

$ firewall-cmd --reload
```

拒绝192.168.1.0段的所有ip访问80端口
```bash
$ firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.16.1.0/24" port protocol="tcp" port="80" reject'

$ firewall-cmd --reload
```

删除规则
```
$ firewall-cmd --permanent --remove-rich-rule='rule family="ipv4" source address="192.168.1.2" port protocol="tcp" port="80" accept'
```

## 端口转发
开启转发功能：
```
$ vi /etc/sysctl.conf
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

