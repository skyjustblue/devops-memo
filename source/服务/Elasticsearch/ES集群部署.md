# ES集群部署

| 节点名称 | 主机名 | IP地址 |
| --- | -- | -- |
| 节点1 | lwz1 | 192.168.1.152 |
| 节点2 | lwz2 | 192.168.1.156 |
| 节点3 | lwz3 | 192.168.1.136 |

## 机器准备
**三个节点**分别执行：
```bash
# 修改各自的主机名
sudo hostnamectl set-hostname lwz1
sudo hostnamectl set-hostname lwz2
sudo hostnamectl set-hostname lwz3

# 修改hosts文件，每台加入以下全部内容
cat >> /etc/hosts <<EOF
192.168.1.152   lwz1
192.168.1.156   lwz2
192.168.1.136   lwz3
EOF

# 关闭防火墙和selinux
sudo systemctl stop firewalld
sudo systemctl disable firewalld
sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
sudo setenforce 0
```

## 集群部署
### yum安装ES(8.x版本)  
**三个节点**都安装  
[参考单机版安装](./ES%E5%8D%95%E6%9C%BA%E7%89%88%E5%AE%89%E8%A3%85.md)  

### 配置文件修改
**三个节点**分别修改，**注意修改**关键字`node.name` `network.host`
```bash
# 备份原配置文件
mv  /etc/elasticsearch/elasticsearch.yml  /etc/elasticsearch/elasticsearch.yml.bak

# 创建新配置文件
vi  /etc/elasticsearch/elasticsearch.yml
##加入如下内容
cluster.name: linyi-es
node.name: lwz1                     #注意修改为lwz2、lwz3
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
network.host: 192.168.1.152         #注意修改为192.168.1.156、192.168.1.136
http.port: 9200
discovery.seed_hosts: ["192.168.1.152", "192.168.1.156", "192.168.1.136"]
xpack.security.enabled: true
xpack.security.enrollment.enabled: true
xpack.security.http.ssl:
  enabled: false
  keystore.path: certs/http.p12
xpack.security.transport.ssl:
  enabled: true
  verification_mode: certificate
  keystore.path: certs/transport.p12
  truststore.path: certs/transport.p12
cluster.initial_master_nodes: ["lwz1", "lwz2", "lwz3"]
http.host: 0.0.0.0
```
### 同步证书
**节点1**执行
```bash
# 将第一台机器上的证书：/etc/elasticsearch/certs/*.p12 以及 keystore文件/etc/elasticsearch/elasticsearch.keystore同步到其他节点
scp -r /etc/elasticsearch/certs/* lwz2:/etc/elasticsearch/certs/
scp -r /etc/elasticsearch/certs/* lwz3:/etc/elasticsearch/certs/
scp /etc/elasticsearch/elasticsearch.keystore lwz2:/etc/elasticsearch/
scp /etc/elasticsearch/elasticsearch.keystore lwz3:/etc/elasticsearch/
```

### 重启es
**三个节点**执行
```bash
systemctl start elasticsearch
systemctl enable elasticsearch
```

### 重置elastic用户密码
**节点1**执行
```bash
/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
##输出如下
New value: sWoihyejRhx0*ybrJg8s
```

## 监测
### 监测集群状态
**节点1**执行
```bash
# 查看集群成员列表
[root@lwz1 ~]# curl -u elastic:"sWoihyejRhx0*ybrJg8s" -X GET 'http://localhost:9200/_cat/nodes?v'
ip            heap.percent ram.percent cpu load_1m load_5m load_15m node.role   master name
192.168.1.152           13          79  13    0.50    0.51     0.25 cdfhilmrstw *      lwz1
192.168.1.136           10          78   9    0.44    0.44     0.20 cdfhilmrstw -      lwz3
192.168.1.156           11          78  11    0.49    0.44     0.18 cdfhilmrstw -      lwz2

# 查看集群状态
[root@lwz1 ~]# curl -u elastic:"sWoihyejRhx0*ybrJg8s" -X GET 'http://localhost:9200/_cluster/health?pretty'
{
  "cluster_name" : "linyi-es",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 3,
  "number_of_data_nodes" : 3,
  "active_primary_shards" : 1,
  "active_shards" : 2,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}
```
集群状态信息：
- cluster_name：表示集群名称
- status：用来标识集群健康状况，green-健康，yellow-亚健康，red-病态
    - green：所有的主分片和副本分片都已分配。你的集群是 100% 可用的。
    - yellow：所有的主分片已经分片了，但至少还有一个副本是缺失的。不会有数据丢失，所以搜索结果依然是完整的。
    - red：至少一个主分片（以及它的全部副本）都在缺失中。这意味着你在缺少数据：搜索只能返回部分数据，而分配到这个分片上的写入请求会返回一个异常。

- number_of_nodes：节点数量，包括master、data、client节点
- number_of_data_nodes：data节点数量
- active_primary_shards：活跃的主分片数目
- active_shards：活跃的分片数，包括主、从索引的分片

### 监测搜索效率
```bash
[root@lwz1 ~]# curl -u elastic:"sWoihyejRhx0*ybrJg8s" -X GET 'http://localhost:9200/kibana_sample_data_logs/_stats?pretty' | less

# 搜索/search
"search" : {
        "open_contexts" : 0,
        "query_total" : 0,
        "query_time_in_millis" : 0,
        "query_current" : 0,
        "fetch_total" : 0,
        "fetch_time_in_millis" : 0,
        "fetch_current" : 0,
        "scroll_total" : 0,
        "scroll_time_in_millis" : 0,
        "scroll_current" : 0,
        "suggest_total" : 0,
        "suggest_time_in_millis" : 0,
        "suggest_current" : 0
      },
```
说明：
- query_current：集群当前正在处理的查询计数。
- fetch_current：集群中正在进⾏的fetch计数。
- query_total：集群处理的所有查询的聚合数。
- query_time_in_millis：所有查询消耗的总时间（以毫秒为单位）。
- fetch_total：集群处理的所有fetch的聚合数。
- fetch_time_in_millis：所有fetch消耗的总时间（以毫秒为单位）。

### 监测节点性能指标
监视文档的索引速率（indexing rate）和合并时间（merge time）有助于在开始影响集群性能之前提前识别异常和相关问题。将这些指标与每个节点的运⾏状况并⾏考虑，这些指标为系统内的潜在问题提供重要线索，为性能优化提供重要参考。
```bash
[root@lwz1 ~]# curl -u elastic:"sWoihyejRhx0*ybrJg8s" -X GET 'http://localhost:9200/_nodes/stats?pretty' | less
#搜索/merges
        "merges" : {
          "current" : 0,
          "current_docs" : 0,
          "current_size_in_bytes" : 0,
          "total" : 7,
          "total_time_in_millis" : 2160,
          "total_docs" : 6937,
          "total_size_in_bytes" : 3850702,
          "total_stopped_time_in_millis" : 0,
          "total_throttled_time_in_millis" : 0,
          "total_auto_throttle_in_bytes" : 440401920
        },
        "refresh" : {
          "total" : 287,
          "total_time_in_millis" : 9033,
          "external_total" : 177,
          "external_total_time_in_millis" : 9283,
          "listeners" : 0
        },
        "flush" : {
          "total" : 51,
          "periodic" : 50,
          "total_time_in_millis" : 2908
        },
```
说明：
- refresh.total：刷新总数的计数。
- refresh.total_time_in_millis：刷新总时间，汇总所有花在刷新的时间（以毫秒为单位进⾏测量）。
- merges.current_docs：合并⽬前正在处理中的文档数。
- merges.total_docs：合并总文档数的计数。
- merges.total_time_in_millis：合并花费的总时间。

### 监测节点JVM运行状况
JVM在其堆分配中管理其内存，并通过GC（garbage collection）进⾏垃圾回收处理。

JVM内存分配给不同的内存池（young old survivor）。需要密切注意这些池中的每个池，以确保它们得到充分利⽤并且没有被超限利⽤的⻛险。  
垃圾收集器（GC）很像物理垃圾收集服务。我们希望让它定期运⾏，并确保系统不会让它过载。

可以通过GET /_nodes/stats 命令检索JVM度量标准。
```bash
[root@lwz1 ~]# curl -u elastic:"sWoihyejRhx0*ybrJg8s" -X GET 'http://localhost:9200/_nodes/stats?pretty' | less
#搜索jvm
      "jvm" : {
        "timestamp" : 1709882469744,
        "uptime_in_millis" : 6292545,
        "mem" : {
          "heap_used_in_bytes" : 181825960,
          "heap_used_percent" : 4,
          "heap_committed_in_bytes" : 4177526784,
          "heap_max_in_bytes" : 4177526784,
          "non_heap_used_in_bytes" : 256334528,
          "non_heap_committed_in_bytes" : 276103168,
          "pools" : {
            "young" : {
              "used_in_bytes" : 37748736,
              "max_in_bytes" : 0,
              "peak_used_in_bytes" : 2483027968,
              "peak_max_in_bytes" : 0
            },
            "old" : {
              "used_in_bytes" : 125829120,
              "max_in_bytes" : 4177526784,
              "peak_used_in_bytes" : 125829120,
              "peak_max_in_bytes" : 4177526784
            },
            "survivor" : {
              "used_in_bytes" : 18248104,
              "max_in_bytes" : 0,
```