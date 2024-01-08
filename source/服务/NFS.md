NFS(网络文件系统)，它允许网络中的计算机之间通过网络共享资源。将NFS主机分享的目录，挂载到本地客户端当中，本地NFS的客户端应用可以透明地读写位于远端NFS服务器上的文件，在客户端端看起来，就像访问本地文件一样。

NFS协议基于RPC，NFS协议本身并不提供文件共享，而是使用RPC协议来传输文件。

RPC，基于C/S模型。程序可以使用这个协议请求网络中另一台计算机上某程序的服务而不需知道网络细节，甚至可以请求对方的系统调用。

# 服务端
1. 安装NFS
    ```
    yum install -y nfs-utils
    ```
2. 创建共享目录
    ```
    mkdir /data/nfs
    chmod 777 /data/nfs
    ```
3. 编辑配置文件，共享目录
    ```
    $ vim /etc/exports

    /data/nfs 192.168.1.0/24(rw,sync,all_squash,anonuid=1000,anongid=1000)
    ```
    > 配置解析：
    > - /data/nfs：共享目录
    > - 192.168.1.0/24：允许连接的客户端地址，*表示所有
    > - rw|ro：允许读写|只读
    > - sync|async：数据会同步写入内存和硬盘|表示数据暂存内存中，不直接写入硬盘
    > - no_root_squash|root_squash：如果是root的登录，会具有root权限|默认情况，使用root会以匿名者使用
    > - all_squash：所有访问用户都映射成匿名用户或用户组
    > - anonuid，anongid 指定匿名用户的UID和pid
4. 启动NFS服务
    ```
    systemctl start nfs-server
    ```
5. 设置开机启动
    ```
    systemctl enable nfs-server.service
    ```

# 客户端
1. 查看服务端的共享目录
    ```
    showmount -e 192.168.1.152
    ```
2. 挂载共享目录
    ```
    mount -t nfs 192.168.1.152:/data/nfs /mnt/nfs
    ```
    永久挂载
    ```
    $ vim /etc/fstab

    192.168.1.152:/data/nfs /mnt/nfs nfs defaults 0 0
    ```
    > 挂载完成后，不管在哪端修改或者创建文件，都会同步到对方。

# exportfs命令管理NFS
选项：
- -a：全部挂载或卸载
- -r：重新挂载
- -u：卸载某目录
- -v：显示共享目录

`exportfs -arv`重新加载NFS配置文件
`exportfs -u /data/nfs`卸载指定共享目录
`mount -t nfs -oremount,ro 192.168.1.152:/root/nfs/nfsdir /mnt/`在客户端上修改NFS共享目录的权限，使其只读
