# selinux

查看状态
```
$ getenforce
Enforcing           # 开启
Disabled            # 关闭
Permission Denied   # 开启但不阻断
```

临时关闭selinux
```
$ setenforce 0
```

永久关闭
```
$ vi /etc/selinux/config
SELINUX=disabled            # SELINUX=enforcing 为开启
```

