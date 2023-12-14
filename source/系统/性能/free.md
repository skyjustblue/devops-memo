# free - 内存状态
free命令 用于显示内存状态。

free命令显示系统内存的使用情况，包括物理内存、交换内存(swap)

用法：
```
[root@lwz1 ~]# free -h
              total        used        free      shared  buff/cache   available
Mem:          7.8Gi       198Mi       7.2Gi        16Mi       440Mi       7.3Gi
Swap:         8.0Gi          0B       8.0Gi
```
- total：内存总数
- used：已经使用的内存数
- free：空闲的内存数
- shared：多个进程共享的内存总额
- buffers/cache：系统用于缓存和缓冲的内存数
- available：可用的物理内存数   

total=used+free+buff/cache