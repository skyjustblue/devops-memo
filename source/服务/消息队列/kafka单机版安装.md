# Kafka单机版安装

## 安装jdk
[jdk安装跳转](https://linyi.readthedocs.io/zh/latest/%E6%9C%8D%E5%8A%A1/Tomcat/%E5%AE%89%E8%A3%85.html#jdk)  
如已安装则跳过此步骤

## 安装和配置kafka
```bash
# 下载、解压
cd /usr/local
sudo wget https://archive.apache.org/dist/kafka/3.6.1/kafka_2.13-3.6.1.tgz
sudo tar zxf kafka_2.13-3.6.1.tgz

# 启动zk服务
cd /usr/local/kafka_2.13-3.6.1/
./bin/zookeeper-server-start.sh config/zookeeper.properties >/dev/null &
# 启动kafka服务
./bin/kafka-server-start.sh config/server.properties >/dev/null &

# 检测服务和端口
pgrep java
netstat -ltnp | grep java
##可以看到9092和2181端口
```

## 验证
```bash
# 创建topic lwz，副本和分区都为1
./bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic lwz

# 查看topic
./bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# 启动生产者，产生消息到lwz这个topic里
[root@lwz1 kafka_2.13-3.6.1]# ./bin/kafka-console-producer.sh --broker-list localhost:9092 --topiclwz
>hello
>lwz
>123456a
>789987b

# 另启一个终端，启动消费者，消费lwz这个topic的消息
[root@lwz1 ~]# cd /usr/local/kafka_2.13-3.6.1
[root@lwz1 kafka_2.13-3.6.1]# ./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic lwz --from-beginning
hello
lwz
123456a
789987b
linyi
##生成者继续增加消息，可以看到消费者动态消费
```
