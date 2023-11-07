# Ubuntu运行级别

ubuntu运行级别：
```
lwz@ubuntu1:~$ ll /lib/systemd/system/runlevel*.target
lrwxrwxrwx 1 root root 15 Mar 20  2023 /lib/systemd/system/runlevel0.target -> poweroff.target
lrwxrwxrwx 1 root root 13 Mar 20  2023 /lib/systemd/system/runlevel1.target -> rescue.target
lrwxrwxrwx 1 root root 17 Mar 20  2023 /lib/systemd/system/runlevel2.target -> multi-user.target
lrwxrwxrwx 1 root root 17 Mar 20  2023 /lib/systemd/system/runlevel3.target -> multi-user.target
lrwxrwxrwx 1 root root 17 Mar 20  2023 /lib/systemd/system/runlevel4.target -> multi-user.target
lrwxrwxrwx 1 root root 16 Mar 20  2023 /lib/systemd/system/runlevel5.target -> graphical.target
lrwxrwxrwx 1 root root 13 Mar 20  2023 /lib/systemd/system/runlevel6.target -> reboot.target
```
- 0是关机；
- 1是救援模式；
- 2.3.4都是多用户命令行模式；
- 5是装完系统后的图形化模式；
- 6是重启
<br>

查看系统当前级别：
```
lwz@ubuntu1:~$ sudo systemctl get-default  
graphical.target
```

修改当前级别为命令行模式：
```
lwz@ubuntu1:~$ sudo systemctl set-default multi-user.target    
```
