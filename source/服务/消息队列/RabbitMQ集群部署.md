# RabbitMQ集群部署
## 集群相关常识
RabbitMQ本身是基于Erlang编写的，Erlang天生支持分布式（通过同步Erlang集群各节点的cookie来实现），因此不需要像Kafka那样通过ZooKeeper来实现分布式集群。

元数据  
RabbitMQ内部有各种基础构件，包括队列、交换器、绑定、虚拟主机等，他们组成了AMQP协议消息通信的基础，而这些构件以元数据的形式存在

内存节点与磁盘节点  
在集群中的每个节点，要么是内存节点，要么是磁盘节点，如果是内存节点，会将所有的元数据信息仅存储到内存中，而磁盘节点则不仅会将所有元数据存储到内存上， 还会将其持久化到磁盘。所以在搭建集群的时候，为了保证数据的安全性和性能，最好是两种节点都要有

## 集群搭建
### 机器规划

| 节点 | 主机名 | IP地址 | 角色 |
| --- | --- | --- | --- |
| 节点1 | lwz1 | 192.168.1.152 | 磁盘节点 |
| 节点2 | lwz2 | 192.168.1.156 | 内存节点 |
| 节点3 | lwz3 | 192.168.1.136 | 内存节点 |

### 环境准备
(三台节点分别执行)
```bash
# 修改各自的主机名
sudo hostnamectl set-hostname lwz1
sudo hostnamectl set-hostname lwz2
sudo hostnamectl set-hostname lwz3

# 修改hosts文件，每台加入以下全部内容
sudo vim /etc/hosts

192.168.1.152   lwz1
192.168.1.156   lwz2
192.168.1.136   lwz3

# 关闭防火墙和selinux
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
sudo setenforce 0
```

### 搭建
1. [安装erlang和RabbitMQ](./RabbitMQ%E5%8D%95%E6%9C%BA%E7%89%88%E5%AE%89%E8%A3%85.md) （三台节点都安装）  

2. 开启web控制台 （三台节点都开启）

3. 创建用户设置权限 （只需在节点1上操作）

4. 将节点1上的cookie文件拷贝到另外两个节点 （节点1上操作）
    ```bash
    scp  /var/lib/rabbitmq/.erlang.cookie lwz2:/var/lib/rabbitmq/.erlang.cookie
    scp  /var/lib/rabbitmq/.erlang.cookie lwz3:/var/lib/rabbitmq/.erlang.cookie
    ```
5. 加入集群 （节点2和节点3上操作）
    ```bash
    # 修改文件属主
    chown rabbitmq /var/lib/rabbitmq/.erlang.cookie
    # 重启rabbitmq-server服务，因为更改了cookie文件内容
    systemctl restart rabbitmq-server
    # 停止应用 -> 加入节点1 -> 启动应用
    rabbitmqctl stop_app
    rabbitmqctl join_cluster --ram rabbit@lwz1
    rabbitmqctl start_app
    ```
6. 查看集群状态
    ```bash
    # 查看集群状态
    [root@lwz3 local]# rabbitmqctl cluster_status
    ##以下为状态输出内容
    Cluster status of node rabbit@lwz3 ...
    Basics

    Cluster name: rabbit@lwz3
    Total CPU cores available cluster-wide: 6

    Disk Nodes

    rabbit@lwz1

    RAM Nodes

    rabbit@lwz2
    rabbit@lwz3

    Running Nodes

    rabbit@lwz1
    rabbit@lwz2
    rabbit@lwz3

    Versions

    rabbit@lwz3: RabbitMQ 3.13.0 on Erlang 26.2.2
    rabbit@lwz1: RabbitMQ 3.13.0 on Erlang 26.2.2
    rabbit@lwz2: RabbitMQ 3.13.0 on Erlang 26.2.2

    CPU Cores

    Node: rabbit@lwz3, available CPU cores: 2
    Node: rabbit@lwz1, available CPU cores: 2
    Node: rabbit@lwz2, available CPU cores: 2

    Maintenance status

    Node: rabbit@lwz3, status: not under maintenance
    Node: rabbit@lwz1, status: not under maintenance
    Node: rabbit@lwz2, status: not under maintenance
    ```

### RabbitMQ其他设置
**设置nodename**  
如果不设置，会根据系统的hostname来定义，但如果系统定义的hostname里面含有点，就会出错，因为rabbitmq只截取第一个点前面的部分
```bash
# 每台节点修改为自己的主机名
vi  /etc/rabbitmq/rabbitmq-env.conf
##添加如下内容
NODENAME=rabbit@lwz1

# 重启rabbitmq服务
systemctl restart rabbitmq-server
```
**更改节点类型（disk或者ram）**
```bash
# 将ram改为disk类型（所有节点都改）
rabbitmqctl  stop_app
rabbitmqctl change_cluster_node_type disc
rabbitmqctl  start_app

# 改完可在状态中查看
rabbitmqctl cluster_status
```