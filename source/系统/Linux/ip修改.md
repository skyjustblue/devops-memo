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
