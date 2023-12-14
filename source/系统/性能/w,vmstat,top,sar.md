# w - 负载、登陆信息

**w命令**用来详细显示登陆当前服务器用户的信息，和系统负载情况。

## 语法及选项

```shell
w [选项]

    选项：
        -f：不显示用户从何处登陆，即：不显示from信息
        -h：不显示标题行
        -s：不显示闲置时间（sleeping）
```

## 实例及详解
```shell
[root@lwz1 sed]# w
 15:02:54 up 26 days, 22:27,  2 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     tty1     -                1511月23 21days  0.00s  0.00s -bash
root     pts/0    192.168.1.110    2011月23  0.00s  2.47s  0.00s w
```
- `15:02:54`：系统当前时间
- `up 26 days, 22:27`：开机到现在经过时间
- `2 users`：当前登录用户数
- `load average: 0.00, 0.00, 0.00`：系统CPU负载，即任务队列长度，三个数值分别为1分钟、5分钟、15分钟前到现在的平均值。（当数值超过当前系统内核数2倍的时候[即：逻辑CPU颗数*2]，表示系统已经有压力）。
- `USER`：登陆的用户名
- `TTY`：登陆的终端类型
- `FROM`：登陆的来源，ip
- `LOGIN@`：登陆时间
- `IDLE`：用户空闲时间
- `JCPU`：进程占用时间
- `PCPU`：用户占用时间 
- `WHAT`：正在执行的进程

### 查看cpu核数
```
[root@lwz1 sed]# cat /proc/cpuinfo
processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 45
model name	: Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz
stepping	: 6
microcode	: 0x61d
cpu MHz		: 2600.037
cache size	: 20480 KB
physical id	: 0
siblings	: 1
core id		: 0
cpu cores	: 1
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 13
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush acpi mmx fxsr sse sse2 ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl cpuid pni pclmulqdq ssse3 cx16 pcid sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer aes xsaveavx hypervisor lahf_lm cpuid_fault pti ssbd ibrs ibpb stibp xsaveopt flush_l1d
bugs		: cpu_meltdown spectre_v1 spectre_v2 spec_store_bypass l1tf
bogomips	: 5200.13
clflush size	: 64
cache_alignment	: 64
address sizes	: 46 bits physical, 48 bits virtual
power management:

processor	: 1
vendor_id	: GenuineIntel
cpu family	: 6
model		: 45
model name	: Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz
stepping	: 6
microcode	: 0x61d
cpu MHz		: 2600.037
cache size	: 20480 KB
physical id	: 1
siblings	: 1
core id		: 0
cpu cores	: 1
apicid		: 2
initial apicid	: 2
fpu		: yes
fpu_exception	: yes
cpuid level	: 13
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush acpi mmx fxsr sse sse2 ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl cpuid pni pclmulqdq ssse3 cx16 pcid sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer aes xsaveavx hypervisor lahf_lm cpuid_fault pti ssbd ibrs ibpb stibp xsaveopt flush_l1d
bugs		: cpu_meltdown spectre_v1 spectre_v2 spec_store_bypass l1tf
bogomips	: 5266.34
clflush size	: 64
cache_alignment	: 64
address sizes	: 46 bits physical, 48 bits virtual
power management:
```
> 这里每一段`processor`代表一个cpu，显示计数从0开始，0代表第一个cpu，1代表第二个cpu，以此类推。

可以直接用下面命令查看具体有几个cpu：
```
[root@lwz1 sed]# grep -c 'processor' /proc/cpuinfo
2
```

# vmstat - 监控系统状态
**vmstat命令**的含义为显示虚拟内存状态(“Viryual Memor Statics”)，但是它可以报告关于进程、内存、I/O等系统整体运行状态。

## 语法及选项
```
vmstat [选项]

    选项：
        -a：显示活动内页；
        -f：显示启动后创建的进程总数；
        -m：显示slab信息；
        -n：头信息仅显示一次；
        -s：以表格方式显示事件计数器和内存状态；
        -d：报告磁盘状态；
        -p：显示指定的硬盘分区状态；
        -S：输出信息的单位。
```

## 示例及详解
```
# 每隔2秒输出一次，不间断，ctrl+c终止
$ vmstat 2 

# 每隔2秒输出一次，输出5次后终止
$ vmstat 2 5
```

详解：
```
[root@lwz1 sed]# vmstat
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0 7589188  61640 347160    0    0     0     0    6    5  0  0 100  0  0
```
> 重点关注`r`,`b`,`si`,`so`,`bi`,`bo`,`wa`。
- `procs`：进程：
    - `r`(run)表示运行或等待CPU时间片的进程数。说明：不要误以为等待CPU时间片意味着这个进程没有进行，实际上某一时刻一个CPU只能有一个进程，其他进程只能排着队等着，此时这些排队等待CPU资源的进程依然是运行状态。该数值如果长期大于服务器CPU的个数，则说明CPU资源不够用了。
    - `b`(block)表示等待资源的进程数，这个资源指的是I/O、内存等。举个例子：当磁盘读写非常频繁时，写数据就会非常慢，此时CPU运算很快就结束了，但进程需要把计算的结果写入磁盘，这样进程的任务才算完成，那此时这个进程只能慢慢地等待，这样这个进程就是这个b状态。该数值如果长时间大于1，则需要关注一下。

- `memory`：内存：
    - `swpd`(swapd)表示切换到交换分区中的内存数量，单位为KB。swpd数据如果持续的变化，说明内存不够用，内存和swap空间（交换分区）持续的在交换数据，如果swpd列有数据变化,si和so列也一定有数据变化。
    - `free`(free)表示当前空闲的内存数量，单位为KB。
    - `buff`(buffers)表示缓冲内存的大小，单位为KB。
    - `cache`(caches)表示缓存内存的大小，单位为KB。

- `swap`：交换分区：
    - `si`(swap in)表示由交换区写入内存的数据量，单位为KB。
    - `so`(swap out)表示由内存写入交换区的数据量，单位为KB。

- `io`：磁盘IO：
    - `bi`(block in)表示从块设备读取数据的量(读磁盘)，单位为KB。
    - `bo`(block out)表示从块设备写入数据的量(写磁盘)，单位为KB。

- `system`显示采集间隔内发生的中断次数：
    - `in`(interrupts)表示在某一时间间隔内观测到的每秒设备的中断次数。
    - `cs`(context switches)表示每秒产生的上下文切换次数。

- `cpu`：CPU使用状态：
    - `us`(user)表示用户进程消耗CPU时间(用户态CPU时间)，单位为百分比。（mysql等服务），如果长时间大于50，表示CPU资源不够。
    - `sy`(system)表示系统进程消耗CPU时间(内核态CPU时间)，单位为百分比。
    - `id`(idle)表示CPU空闲时间，单位为百分比。
    - `wa`(wait)表示等待I/O时间，单位为百分比。如果wa列值比较大，说明等待的进程数比较大，CPU需要增加。
    - `st`(steal)表示被虚拟机偷走的CPU时间，单位为百分比。

------------
# top - 动态监控系统负载

## 详解
```
[root@lwz1 sed]# top
top - 16:55:48 up 27 days, 20 min,  2 users,  load average: 0.00, 0.00, 0.00
Tasks:  89 total,   2 running,  87 sleeping,   0 stopped,   0 zombie
%Cpu(s):  3.1 us,  3.1 sy,  0.0 ni, 93.8 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   7963.6 total,   7410.7 free,    153.7 used,    399.2 buff/cache
MiB Swap:   8192.0 total,   8192.0 free,      0.0 used.   7568.5 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
    1 root      20   0  176272  11004   8304 S   0.0   0.1   0:13.54 systemd
    2 root      20   0       0      0      0 S   0.0   0.0   0:00.50 kthreadd
```
- `top - 16:55:48 up 27 days, 20 min,  2 users,  load average: 0.00, 0.00, 0.00`：系统负载信息。
    - `16:55:48`：当前时间
    - `up 27 days, 20 min`：系统运行时间
    - `2 users`：当前登录用户数
    - `load average: 0.00, 0.00, 0.00`：系统1分钟、5分钟、15分钟的平均负载。
- `Tasks:  89 total,   2 running,  87 sleeping,   0 stopped,   0 zombie`：任务信息。
    - `89 total`：任务总数
    - `2 running`：正在运行的任务数
    - `87 sleeping`：睡眠的任务数
    - `0 stopped`：停止的任务数
    - `0 zombie`：僵尸进程数
- `%Cpu(s):  3.1 us,  3.1 sy,  0.0 ni, 93.8 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st`：CPU信息。
    - `3.1 us`：用户空间占用CPU百分比
    - `3.1 sy`：内核空间占用CPU百分比
    - `0.0 ni`：用户进程空间内改变过优先级的进程占用CPU百分比
    - `93.8 id`：空闲CPU百分比
    - `0.0 wa`：等待输入输出的CPU时间百分比
    - `0.0 hi`：硬中断时间百分比
    - `0.0 si`：软中断时间百分比
    - `0.0 st`：虚拟机占用百分比
- `MiB Mem :   7963.6 total,   7410.7 free,    153.7 used,    399.2 buff/cache`：内存信息。
    - `7963.6 total`：物理内存总量
    - `7410.7 free`：空闲内存总量
    - `153.7 used`：已用内存总量
    - `399.2 buff/cache`：缓冲/缓存内存总量
- `MiB Swap:   4095.0 total,   4095.0 free,      0.0 used.   7394.5 avail Mem`：交换区信息。
    - `4095.0 total`：交换区总量
    - `4095.0 free`：空闲交换区总量
    - `0.0 used`：已用交换区总量
    - `7394.5 avail Mem`：可用交换区总量
- `  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME  COMMAND`：进程信息。
    - `PID`：进程id
    - `USER`：进程所有者
    - `PR`：进程优先级
    - `NI`：nice值，负值表示高优先级，正值表示低优先级
    - `VIRT`：虚拟内存
    - `RES`：进程所占物理内存大小
    - `SHR`：共享内存
    - `S`：进程状态。
        - `R`：正在运行
        - `S`：睡眠
        - `D`：不可中断
        - `Z`：僵尸进程
        - `T`：停止
        - `t`：被追踪
        - `X`：死亡
    - `%CPU`：上次更新到现在的CPU时间占用百分比
    - `%MEM`：进程使用的物理内存百分比
    - `TIME`：进程使用的CPU时间总计
    - `COMMAND`：进程名称

## top命令中的交互命令

- `h`：显示帮助
- `q`：退出
- `M`：按照MEM使用排序
- `P`：按照CPU使用排序
- `T`：按照TIME使用排序
- `1`：多核CPU会按照单个CPU进行展示CPU使用情况

## 常用示例
```
top             
top -d 1        # 指定刷新时间间隔，单位为秒
top -c          # 显示COMAND段的详细信息
top -bn1        # 静态显示，一次性全部打印
top -c -bn1
```

# sar - 监控网卡流量状态
**sar命令**很强大，它可以监控系统所有资源状态，比如平均负载、网卡流量、磁盘状态、内存使用等等。它不同于其他系统状态监控工具的地方在于，它可以打印历史信息，可以显示当天从零点开始到当前时刻的系统状态信息。如果你系统没有安装这个命令，请使用 `yum install -y sysstat` 命令安装。初次使用sar命令会报错，那是因为sar工具还没有生成相应的数据库文件(时时监控就不会了，因为不用去查询那个库文件)。它的数据库文件在 “/var/log/sa/” 目录下，默认保存一个月。

## 示例
查看网卡流量
```
[root@lwz1 sed]# sar -n DEV
Linux 4.18.0-80.el8.x86_64 (lwz1) 	2023年12月07日 	_x86_64_	(2 CPU)

00时00分50秒     IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
00时10分07秒        lo      0.00      0.00      0.00      0.00      0.00      0.00      0.000.00
00时10分07秒      eth0      2.38      0.15      0.23      0.01      0.00      0.00      0.000.00
00时20分07秒        lo      0.00      0.00      0.00      0.00      0.00      0.00      0.000.00
00时20分07秒      eth0      2.29      0.07      0.21      0.00      0.00      0.00      0.000.00
```
- `IFACE`：网卡名称
- `rxpck/s`：每秒收到数据包数量
- `txpck/s`：每秒发出数据包数量
- `rxkB/s`：每秒收到数据量(KB)
- `txkB/s`：每秒发出数据量(KB)

> 剩下后面几列不需要关注。如果有一天你所管理的服务器丢包非常严重，那么你就应该看一看这个网卡流量是否异常了，如果rxpck/s 那一列的数值大于4000，或者rxbyt/s那列大于5,000,000则很有可能是被攻击了，正常的服务器网卡流量不会高于这么多，除非是你自己在拷贝数据。


```
$ sar -n DEV 2 5        # 每隔2秒输出一次流量状态，5次后终止

$ sar -n DEV -f /var/log/sa/sa**    # 查看某一天的流量信息
```
> 在Red Hat或者CentOS发行版中，sar的库文件一定在/var/log/sa/目录下的saxx目录，xx代表日期。

```
$ sar -q            # 查看系统负载

$ sar -b            # 查看I/O和传送速率

$ sar -B           # 查看缓冲区使用情况

$ sar -w            # 显示交换分区使用情况
```

# nload - 动态查看网卡流量
安装：
```
$ yum install -y epel-release
$ yum install -y nload
```
执行：
```
$ nload     
```
`Incoming`为进入网卡的流量。    
`Outgoing`为网卡出去的流量。      

主要关注`Curr`那行的数据，其单位也可以动态自动调整。    

按`q`退出该界面。   
