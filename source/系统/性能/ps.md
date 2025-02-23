# ps - 进程信息
**ps命令**来自于英文词组”process status“的缩写，其功能是用于显示当前系统的进程状态。使用ps命令可以查看到进程的所有信息，例如进程的号码、发起者、系统资源使用占比（处理器与内存）、运行状态等等。帮助我们及时的发现哪些进程出现”僵死“或”不可中断“等异常情况。  

经常会与kill命令搭配使用来中断和删除不必要的服务进程，避免服务器的资源浪费。

## 语法及选项
```
ps [选项]

    常用选项：
        a：显示所有程序，包括其他用的程序；
        u：以用户为主的格式来显示程序状态；
        x：以用户与程序共同的信息来显示程序状态；
        -A：列出所有的行程；
        c：显示每个程序真正的指令名称，而不包含路径；
        e：显示环境变量；
        l：显示进程的详细信息；
        f：显示进程间的关系；
        -H：显示树状结构；
        r：显示当前终端的进程；

    其他选项：
        -e：等价于“-A”，即显示所有进程；
        -f：显示进程间的关系；
        -h：显示树状结构；
        -l：显示进程的详细信息；
        -w：显示加宽，可以显示更多的信息；
        -p：指定进程号，即显示指定进程的信息；
        -s：指定进程号，即显示指定进程的子进程；
        -t：指定终端号，即显示指定终端的进程；
        -j：显示进程的job信息；
        -o：指定输出格式，例如：
            user：显示用户名
            pid：显示进程号
            lwp：显示轻量级进程号
            ppid：显示父进程号
            pgid：显示进程组ID
            sid：显示会话ID
            pri：显示进程优先级
            nice：显示进程nice值
            psr：显示当前进程的CPU使用率
            %cpu：显示进程的CPU使用率
            %mem：显示进程的内存使用率
            etime：显示进程的运行时间
```

## 示例
### 列出进程的详细信息
```
[root@lwz1 sed]# ps -elf
F S UID        PID  PPID  C PRI  NI ADDR SZ WCHAN  STIME TTY          TIME CMD
4 S root         1     0  0  80   0 - 44103 do_epo 11月09 ?      00:00:14 /usr/lib/systemd/system
1 S root         2     0  0  80   0 -     0 -      11月09 ?      00:00:00 [kthreadd]
1 I root         3     2  0  60 -20 -     0 -      11月09 ?      00:00:00 [rcu_gp]
```
解释：
- F：进程的标志，与ps -ef的输出格式相同；
- S：进程的状态：
    - S：睡眠；
    - D：不可中断休眠（IO）；
    - R：正在运行；
    - Z：僵尸进程；
    - T：停止；
    - I：空闲内核线程；
    - s：包含子进程；
- UID：进程所有者的用户名；
- PID：进程ID；
- PPID：父进程ID；
- C：进程使用的CPU时间；
- PRI：进程的优先级；
- NI：进程的优先级；
- ADDR：进程的内存地址；
- SZ：进程使用内存大小；
- WCHAN：进程休眠的资源；
- STIME：进程启动的时间；
- TTY：进程启动时的终端；
- TIME：进程使用的CPU时间；
- CMD：命令名/命令行;


### 列出所有终端的所有用户的所有进程：
```
[root@lwz1 sed]# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 176412 11040 ?        Ss   11月09   0:14 /usr/lib/systemd/systemd --swit
root         2  0.0  0.0      0     0 ?        S    11月09   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        I<   11月09   0:00 [rcu_gp]
```
解释：
- USER：进程所有者的用户名；
- PID：进程ID；
- %CPU：进程占用的CPU使用率；
- %MEM：进程使用的物理内存比例；
- VSZ：进程使用的虚拟内存大小；
- RSS：进程使用的物理内存大小；
- TTY：进程的终端号；
- STAT：进程状态；
    - <：高优先级；
    - N：低优先级；
    - L：被锁；
    - S：进程的睡眠状态；
    - R：正在运行；
    - I：空闲内核线程；
    - +：在后台进程组里；
- START：进程启动时间；
- TIME：进程使用的CPU时间；
- COMMAND：命令名/命令行;

