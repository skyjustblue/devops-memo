# screen - 后台执行工具
当我们需要执行一个任务很长时间的时候，我们不可以与从远程终端当中退出，有什么办法可以让任务继续进行，并且任务不会断开呢，可以使用`nohup command >> 1.log &`这样一种方法把任务放置于后台进行，当想查看屏幕上的信息的时候是无法查看到，这就可以使用screen工具来开启一个新的虚拟终端。  
系统默认screen是没有安装的，需要安装下
```
yum install -y screen
```

运行命令screen即可开启一个虚拟终端
```
# 命令screen即可开启一个虚拟终端
$ screen

# 查看虚拟终端
$ screen -ls

# 使用-r选项加上终端的ID号即可回到终端
$ screen -r 1234

# 有多个screen很久了，不知道那个是我需要的，该怎么办呢，可以在创建screen的时候加上-S选项，指定一个名字
$ screen -S lwz
$ screen -r lwz             # 指定回到lwz这个终端

# 退出终端
$ exit
```
