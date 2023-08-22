# swapfile扩容

首先，使用以下命令关闭swap：

    $ sudo swapoff -a

然后，使用以下命令删除旧的swapfile：

    $ sudo rm /swapfile

接下来，创建一个新的swapfile，并设置所需的大小（以MB为单位）。例如，要创建一个大小为4GB的swapfile，可以使用以下命令：

    $ sudo fallocate -l 4G /swapfile

设置新的swapfile的权限：

    $ sudo chmod 600 /swapfile

使用以下命令将新的swapfile设置为swap区域：

    $ sudo mkswap /swapfile

最后，启用新的swapfile：

    $ sudo swapon /swapfile

现在，你的swapfile已经成功扩容了。你可以使用以下命令来验证swap是否已经启用：

    $ sudo swapon --show

**记住，修改swapfile大小可能会对系统性能产生影响，请提前备份，谨慎操作。**
