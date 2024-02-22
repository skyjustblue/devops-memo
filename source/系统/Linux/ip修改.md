# IP修改

## ubuntu23.04修改ip
网卡原文件dhcp模式：
```
# This is the network config written by 'subiquity'
network:
  ethernets:
    enX3:
      dhcp4: true
  version: 2
```

修改为手动设置：
```
lwz@ubuntu1:~$ sudo cp /etc/netplan/00-installer-config.yaml{,.bak}     # 先备份一下原文件

lwz@ubuntu1:~$ sudo vi /etc/netplan/00-installer-config.yaml    # 修改网卡配置文件
# This is the network config written by 'subiquity'
network:
  ethernets:
    enX3:
      dhcp4: no
      addresses: [192.168.1.153/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [10.16.32.11,10.16.32.12]
  version: 2
```

重启网卡信息：
```
lwz@ubuntu1:~$ sudo netplan apply
```

## Rocky8修改ip
配置文件中设置手动ip地址（centos7也适用）
```
# 修改配置文件
sudo vi /etc/sysconfig/network-scripts/ifcfg-eth0

TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=eth0
UUID=2bc9822a-9638-47cf-b39b-f2fe6facd47e
DEVICE=eth0
ONBOOT=yes
IPADDR=192.168.1.136
NETMASK=255.255.255.0
GETEWAY=192.168.1.1
DNS1=10.16.32.11
DNS2=10.16.32.12

# 重启网络服务
systemctl restart NetworkManager

# 生效新的ip地址
nmcli c up eth0
```
Rocky8网卡操作命令：  
- 重载网卡配置：`nmcli connection reload` 
- 开启网卡：`nmcli c up ens33`
- 关闭网卡：`nmcli c down ens33`
- 查看网卡的配置信息和运行状态：`nmcli`
- 查看网卡的状态：`nmcli device status`
- 查看所有网卡设备详细信息：`nmcli device show`
- 查看ens33网卡设备详细信息：`nmcli device show ens33`
- 为网卡添加静态IP地址：`nmcli c modify ens33+ipv4.address10.0.0.200/8`（将10.0.0.200替换为所需的IP地址）
- 使新的IP地址生效：`nmcli c up ens33`
