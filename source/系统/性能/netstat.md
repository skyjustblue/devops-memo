# netstat - 查看网络状态
**netstat命令**来自于英文词组”network statistics“的缩写，其功能是用于显示各种网络相关信息，例如网络连接状态、路由表信息、接口状态、NAT、多播成员等等。   

netstat命令不仅应用于Linux系统，而且在Windows XP、Windows 7、Windows 10及Windows 11中均已默认支持，并且可用参数也相同。

## 语法及选项
```
# netstat在net-tools包中，有些系统需要手动安装
yum install net-tools -y
```

```
netstat [选项]

    选项：
        -a：显示所有连线中的Socket；
        -p：显示正在使用Socket的程序识别码和程序名称；
        -l：显示正在Listener的Socket；
        -t：显示TCP传输协议的连线状况；
        -u：显示UDP传输协议的连线状况；
        -i：显示网络界面信息表单；
        -r：显示路由表内容。
        -n：直接显示IP地址，而不通过域名服务器；
```

## 示例

```
$ netstat -lnp            # 查看监听的端口

$ netstat -an             # 查看系统的网络连接状况

$ netstat -lntp           # 只看tcp的，不包含socket，这条更方便查看端口监听状态

$ netstat -lntup          # 只查看与外部的tcp连接

$ netstat -rn             # 显示路由表

$ netstat -rn --fib       # 显示路由表，并显示fib表
```
