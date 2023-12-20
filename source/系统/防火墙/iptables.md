# iptables

iptables 是 Linux 防火墙系统的重要组成部分，iptables 的主要功能是实现对网络数据包进出设备及转发的控制。当数据包需要进入设备、从设备中流出或者由该设备转发、路由时，都可以使用 iptables 进行控制。

## 简介

iptables 是集成在 Linux 内核中的包过滤防火墙系统。使用 iptables 可以添加、删除具体的过滤规则，iptables 默认维护着 4 个表和 5 个链，所有的防火墙策略规则都被分别写入这些表与链中。  

“四表”是指 iptables 的功能，默认的 iptable s规则表有 filter 表（过滤规则表）、nat 表（地址转换规则表）、mangle（修改数据标记位规则表）、raw（跟踪数据表规则表）：

**四表：**

|表名|含义|
|:--|:--|
|filter|过滤规则表： 包含INPUT、FORWARD、OUTPUT三条链|
|nat|地址转换规则表： 包含PREROUTING、INPUT、OUTPUT、POSTROUTING四条链|
|mangle|修改数据标记位规则表： 包含PREROUTING、INPUT、OUTPUT、POSTROUTING、FORWARD五条链|
|raw|跟踪数据表规则： 包含PREROUTING、OUTPUT两条链|

- **filter 表**：控制数据表是否允许进出及转发，可以控制的链路有：INPUT、FORWARD、OUTPUT。
- **nat 表**：控制数据包的地址转换，可以控制的链路有：PREROUTING、INPUT、OUTPUT、POSTROUTING。
- **mangle 表**：修改数据包中的原数据，可以控制的链路有：PREROUTING、INPUT、OUTPUT、FORWARD、POSTROUTING。
- **raw 表**：控制nat表中连接追踪机制的启用状况，可以控制的链路有：PREROUTING、OUTPUT。

“五链”是指内核中控制网络的 NetFilter 定义的 5 个规则链。每个规则表中包含多个数据链：INPUT（入站数据过滤）、OUTPUT（出站数据过滤）、FORWARD（转发数据过滤）、PREROUTING（路由前过滤）和POSTROUTING（路由后过滤），防火墙规则需要写入到这些具体的数据链中。

**五链：**

|链名|含义|
|:--|:--|
|INPUT|进来的数据包应用此规则链中的策略|
|OUTPUT|出去的数据包应用此规则链中的策略|
|FORWARD|转发数据包应用此规则链中的策略|
|PREROUTING|对数据包作路由选择前应用此链中的规则（所有的数据包进来的时侯都先由这个链处理）|
|POSTROUTING|对数据包作路由选择后应用此链中的规则（所有的数据包出去的时候都先由这个链处理）|

**iptables传输数据包的过程**
1. 当一个数据包进入网卡时，它首先进入PREROUTING链，内核根据数据包目的IP判断是否需要转送出去。  
2. 如果数据包就是进入本机的，它就会沿着图向下移动，到达INPUT链。数据包到了INPUT链后，任何进程都会收到它。本机上运行的程序可以发送数据包，这些数据包会经过OUTPUT链，然后到达POSTROUTING链输出。 
3. 如果数据包是要转发出去的，且内核允许转发，数据包就会如图所示向右移动，经过FORWARD链，然后到达POSTROUTING链输出。

**规则表之间的优先顺序：**  
Raw——mangle——nat——filter 规则链之间的优先顺序（分三种情况）：  

**第一种情况：入站数据流向**  
从外界到达防火墙的数据包，先被PREROUTING规则链处理（是否修改数据包地址等），之后会进行路由选择（判断该数据包应该发往何处），如果数据包 的目标主机是防火墙本机（比如说Internet用户访问防火墙主机中的web服务器的数据包），那么内核将其传给INPUT链进行处理（决定是否允许通 过等），通过以后再交给系统上层的应用程序（比如Apache服务器）进行响应。  

**第二冲情况：转发数据流向**   
来自外界的数据包到达防火墙后，首先被PREROUTING规则链处理，之后会进行路由选择，如果数据包的目标地址是其它外部地址（比如局域网用户通过网 关访问QQ站点的数据包），则内核将其传递给FORWARD链进行处理（是否转发或拦截），然后再交给POSTROUTING规则链（是否修改数据包的地 址等）进行处理。  

**第三种情况：出站数据流向**   
防火墙本机向外部地址发送的数据包（比如在防火墙主机中测试公网DNS服务器时），首先被OUTPUT规则链处理，之后进行路由选择，然后传递给POSTROUTING规则链（是否修改数据包的地址等）进行处理。

## 安装
```
$ yum install iptables-services
```

## 启动关闭
```
# 启动|关闭|重启
$ systemctl start|stop|restart iptables
或者
$ service iptables start|stop|restart

# 查看状态
$ systemctl status iptables
或者
$ service iptables status

# 开机启动|禁用
$ systemctl enable|disable iptables
或者
$ chkconfig iptables on|off
```

## 语法
```
iptables [-t 表名] 管理选项 [链名] [匹配条件] [-j 目标动作]

    管理选项：
        -A：在指定链的末尾添加（append）一条新的规则
        -D：删除（delete）一条已有的规则
        -I：在指定链的头部插入（insert）一条新的规则
        -R：修改、替换（replace）已有的规则，可以按规则序号和内容替换
        -L：显示（list）指定链中的所有规则
        -E：重命名用户定义的链，不改变链本身
        -F：清空（flush）指定链中的所有规则
        -N：新建一个用户自定义的链
        -X：删除指定表中用户自定义的规则链（delete-chain）
        -P：设置指定链的默认策略（policy）
        -Z：将所有表的所有链的字节和数据包计数器清零
        -n：使用数字形式（numeric）显示输出结果
        -v：查看规则表详细信息（verbose）的信息
        -V：查看版本信息
        -h：获取帮助

    匹配条件：
        -p：指定协议，如tcp、udp、icmp
        -s：指定源地址，如192.168.1.1/24（IP地址、网络地址、网络地址段）
        -d：指定目标地址
        -i：指定数据包的入站接口
        -o：指定数据包的出站接口
        -m：指定要使用的扩展匹配，如多播、IP范围、IP列表、IP域等

    目标动作：
        ACCEPT：接收数据包
        DROP：丢弃数据包
        REJECT：拒绝数据包，必要时会给数据发送端一个响应信息
        SNAT：源地址转换
        DNAT：目标地址转换
        MASQUERADE：地址伪装
        REDIRECT：重定向
        LOG：日志记录
```

## 实例

### 规则的保存与恢复
```
# 指定规则保存至文件
$ iptables-save > /etc/sysconfig/iptables
或者
$ service iptables save     # 自动把规则保存在/etc/sysconfig/iptables中。
```
> iptables-save把规则保存到文件中，再由目录rc.d下的脚本（/etc/rc.d/init.d/iptables）自动装载。


当计算机启动时，rc.d下的脚本将用命令iptables-restore调用这个文件，从而就自动恢复了规则。  

或者用命令手动恢复：
```
# 恢复规则
$ iptables-restore < /etc/sysconfig/iptables
```

### 规则查看
```
$ iptables -L
```

### 添加规则

**注意先拒绝再允许**

#### 允许
##### 允许防火墙转发除ICMP协议以外的所有数据包
```
$ iptables -A FORWARD -p ! icmp -j ACCEPT
```
> 说明：使用`!`可以将条件取反。

##### 允许防火墙转发所有数据包
```
$ iptables -A FORWARD -j ACCEPT
```

##### 只允许防火墙接收来自192.168.1.0/16网段的SSH数据
```
$ iptables -A INPUT -p tcp --dport 22 -j DROP       # 拒绝所有人访问22端口
$ iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/16 -j ACCEPT
```
> 说明：这个用法比较适合对设备进行远程管理时使用，比如位于分公司中的SQL服务器需要被总公司的管理员管理时。

##### 允许本机开放从tcp端口20-1024提供的应用服务
```
$ iptables -A INPUT -p tcp --dport 20:1024 -j ACCEPT
$ iptables -A OUTPUT -p tcp --sport 20:1024 -j ACCEPT
```

##### 允许防火墙本机对外开放TCP端口20、21、25、110以及被动模式FTP端口1250-1280
```
$ iptables -A INPUT -p tcp -m multiport --dport 20,21,25,110,1250:1280 -j ACCEPT
```
> 说明：这里用“-m multiport –dport”来指定目的端口及范围。

##### 只开放本机的web服务（80）、FTP(20、21、20450-20480)，放行外部主机发往服务器其它端口的应答数据包，将其他入站数据包均予以丢弃处理
```
$ iptables -I INPUT -p tcp -m multiport --dport 20,21,80 -j ACCEPT
$ iptables -I INPUT -p tcp --dport 20450:20480 -j ACCEPT
$ iptables -I INPUT -p tcp -m state --state ESTABLISHED -j ACCEPT
$ iptables -P INPUT DROP
```

#### 拒绝
##### 拒绝进入防火墙的所有ICMP协议数据包
```
$ iptables -I INPUT -p icmp -j REJECT
```

##### 丢弃从外网接口（eth1）进入防火墙本机的源地址为私网地址的数据包
```
$ iptables -A INPUT -i eth1 -s 192.168.0.0/16 -j DROP
$ iptables -A INPUT -i eth1 -s 172.16.0.0/12 -j DROP
$ iptables -A INPUT -i eth1 -s 10.0.0.0/8 -j DROP
```

##### 封堵网段（192.168.1.0/24），两小时后解封
```
$ iptables -I INPUT -s 192.168.1.0/24 -j DROP
$ iptables -I FORWARD -s 192.168.1.0/24 -j DROP
$ at now 2 hours at> iptables -D INPUT 1 at> iptables -D FORWARD 1
```
> 说明：`at now 2 hours`表示在当前时间2小时后执行`at>`后面的命令。

##### 禁止其他主机ping防火墙主机，但允许从防火墙主机ping其他主机
```
$ iptables -I INPUT -p icmp --icmp-type Echo-Request -j DROP        # 拒绝进入防火墙的所有ICMP协议数据包
$ iptables -I INPUT -p icmp --icmp-type Echo-Reply -j ACCEPT
$ iptables -I INPUT -p icmp --icmp-type Destination-Unreachable -j ACCEPT       # 允许通知发送方目标主机不可达
```

##### 禁止转发来自MAC地址为00：0C：29：27：55：3F的和主机的数据包
```
$ iptables -A FORWARD -m mac --mac-source 00:0C:29:27:55:3F -j DROP
```
> 说明：iptables中使用“-m 模块关键字”的形式调用显示匹配。咱们这里用“-m mac –mac-source”来表示数据包的源MAC地址。

##### 禁止转发源IP地址为192.168.1.20-192.168.1.99的TCP数据包
```
$ iptables -A FORWARD -p tcp -m iprange --src-range 192.168.1.20-192.168.1.99 -j DROP
```
> 说明：此处用“-m –iprange –src-range”指定IP范围。

##### 禁止转发与正常TCP连接无关的非—syn请求数据包。
```
$ iptables -A FORWARD -m state --state NEW -p tcp ! --syn -j DROP
```
> 说明：`-m state`表示数据包的连接状态，“NEW”表示与任何连接无关的。

##### 拒绝访问防火墙的新数据包，但允许响应连接或与已有连接相关的数据包
```
$ iptables -A INPUT -p tcp -m state --state NEW -j DROP
$ iptables -A INPUT -p tcp -m state --state ESTABLISHED,RELATED -j ACCEPT
```
> 说明：`ESTABLISHED`表示已经响应请求或者已经建立连接的数据包，“RELATED”表示与已建立的连接有相关性的，比如FTP数据连接等。

### 删除规则

##### 清除所有规则
```
$ iptables -t nat -F
```

##### 删除INPUT链的第一条规则
```
$ iptables -D INPUT 1
```

