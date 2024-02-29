# Kafka集群部署
机器准备：

| 机器名 | IP地址 | 安装软件 |
| ------ | -------- | ---------- |
| lwz1 | 192.168.1.152 | java, zookeeper, kafka |
| lwz2 | 192.168.1.156 | java, zookeeper, kafka |
| lwz3 | 192.168.1.136 | java, zookeeper, kafka |

环境准备：
```bash
# 设置主机名、hosts、关闭selinux和防火墙
hostnamectl  set-hostname lwz1
hostnamectl  set-hostname lwz2
hostnamectl  set-hostname lwz3

vim /etc/hosts
192.168.1.152	lwz1
192.168.1.156	lwz2
192.168.1.136	lwz3

systemctl stop firewalld
systemctl disable firewalld

setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
```

## 安装java
[jdk安装跳转](https://linyi.readthedocs.io/zh/latest/%E6%9C%8D%E5%8A%A1/Tomcat/%E5%AE%89%E8%A3%85.html#jdk)  
(三台机器都安装)

## 安装zookeeper集群
(三台机器都安装)
```bash
# 下载、解压、软链接
cd /usr/local/
sudo wget https://dlcdn.apache.org/zookeeper/zookeeper-3.8.3/apache-zookeeper-3.8.3-bin.tar.gz
tar zxf apache-zookeeper-3.8.3-bin.tar.gz
ln -s apache-zookeeper-3.8.3-bin/ zookeeper

# 定义配置文件（三台机器内容一样）
sudo vi /usr/local/zookeeper/conf/zoo.cfg

tickTime=2000
initLimit=100
syncLimit=50
dataDir=/usr/local/zookeeper/data
dataLogDir=/usr/local/zookeeper/logs
clientPort=2181
server.1=192.168.1.152:2888:3888
server.2=192.168.1.156:2888:3888
server.3=192.168.1.136:2888:3888

# 创建数据目录和日志目录
sudo mkdir  /usr/local/zookeeper/{data,logs}

# 设置myid（三台机器分别执行一条）
##lwz1执行
echo "1" > /usr/local/zookeeper/data/myid
##lwz2执行
echo "2" > /usr/local/zookeeper/data/myid
##lwz3执行
echo "3" > /usr/local/zookeeper/data/myid

# 启动zookeeper服务
/usr/local/zookeeper/bin/zkServer.sh start

# 查看zookeeper集群状态
/usr/local/zookeeper/bin/zkServer.sh status
```

## kafka集群部署
(三台机器都安装)
```bash
# 下载、解压、软链接
cd /usr/local/
sudo wget https://archive.apache.org/dist/kafka/3.6.1/kafka_2.13-3.6.1.tgz
sudo tar zxf kafka_2.13-3.6.1.tgz
sudo ln -s /usr/local/kafka_2.13-3.6.1 /usr/local/kafka

# 修改配置文件（三台分别修改内容）
sudo vi /usr/local/kafka/config/server.properties
##将配置文件中原有的broker.id和zookeeper.connect注释掉，直接在最后面添加如下内容
##每台机器broker.id不一样，分别修改为1、2、3
broker.id=1
zookeeper.connect=192.168.1.152:2181,192.168.1.156:2181,192.168.1.136:2181

# 启动服务
nohup /usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties &

# 查看进程和端口
##看是否有kafka
jps
##查看是否有9092
netstat -lntp |grep java
```

### 验证
```bash
# 创建topic linyi，副本为2和分区3
[root@lwz1 ~]# /usr/local/kafka/bin/kafka-topics.sh  --create --bootstrap-server lwz2:9092 --replication-factor 2 --partitions 3 --topic linyi
Created topic linyi.

# 列出topic。
[root@lwz1 ~]# /usr/local/kafka/bin/kafka-topics.sh --list --bootstrap-server lwz1:9092
linyi
linyi2
[root@lwz1 ~]# /usr/local/kafka/bin/kafka-topics.sh --list --bootstrap-server lwz3:9092
linyi
linyi2

# 查看topic详情
[root@lwz1 ~]# /usr/local/kafka/bin/kafka-topics.sh  --bootstrap-server lwz3:9092 --topic linyi --describe
Topic: linyi	TopicId: v8LWLkRvT8aPFynsV5H-SQ	PartitionCount: 3	ReplicationFactor: 2	Configs:
	Topic: linyi	Partition: 0	Leader: 2	Replicas: 2,3	Isr: 2,3
	Topic: linyi	Partition: 1	Leader: 3	Replicas: 3,1	Isr: 3,1
	Topic: linyi	Partition: 2	Leader: 1	Replicas: 1,2	Isr: 1,2

##模拟故障
# 杀掉lwz2上的kafka进程
jps | grep -i kafka | awk '{print $1}' | xargs kill

# 再次查看topic详情，发现lwz2下线了
[root@lwz1 ~]# /usr/local/kafka/bin/kafka-topics.sh  --bootstrap-server lwz3:9092 --topic linyi --describe
Topic: linyi	TopicId: v8LWLkRvT8aPFynsV5H-SQ	PartitionCount: 3	ReplicationFactor: 2	Configs:
	Topic: linyi	Partition: 0	Leader: 3	Replicas: 2,3	Isr: 3
	Topic: linyi	Partition: 1	Leader: 3	Replicas: 3,1	Isr: 3,1
	Topic: linyi	Partition: 2	Leader: 1	Replicas: 1,2	Isr: 1

# 启动lwz2上的kafka进程，即可恢复
[root@lwz2 ~]# nohup /usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties &
[root@lwz1 ~]# /usr/local/kafka/bin/kafka-topics.sh  --bootstrap-server lwz3:9092 --topic linyi --describe
Topic: linyi	TopicId: v8LWLkRvT8aPFynsV5H-SQ	PartitionCount: 3	ReplicationFactor: 2	Configs:
	Topic: linyi	Partition: 0	Leader: 3	Replicas: 2,3	Isr: 3,2
	Topic: linyi	Partition: 1	Leader: 3	Replicas: 3,1	Isr: 3,1
	Topic: linyi	Partition: 2	Leader: 1	Replicas: 1,2	Isr: 1,2
```