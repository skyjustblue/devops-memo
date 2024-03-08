# ES配置文件和常用操作

## 修改配置文件
配置文件所在路径：`/etc/elasticsearch/`

```bash
# 修改jvm内存大小
vi /etc/elasticsearch/jvm.options
## -Xms4g
## -Xmx4g
-Xms512m
-Xmx512m
```
> 说明：  
> 默认，ES最高使用系统内存的50%，如果你的服务器还有其它服务，建议配置这两个参数。   
> 建议：两个参数设置为一样，如果不一样可能会导致heap resize时产生停顿，最大内存不要超过机器内存总量的50%（因为要预留内存给lucene进行全文检索），并且最大内存不要超过32G，超过32G会开启一个内存对象指针压缩功能，从而导致性能下降

## 日志文件
- ES日志：默认缺省日志为`/var/log/elasticsearch/elasticsearch.log` ，如果开启了集群（设置了集群名字，如集群部署中的linyi-es），那么日志名字为"/var/log/elasticsearch/linyi-es.log"  

- gc日志：`/var/log/elasticsearch/gc.log`，jvm清除垃圾数据的日志。
- Kibana日志： `/var/log/kibana/kibana.log` ，也可以用journalctl来查看：`journalctl -u kibana --no-p`

## 常用操作
```bash
# 查看集群状态（green表示健康，yellow表示有问题）
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -X GET 'http://localhost:9200/_cluster/health?pretty'
{
  "cluster_name" : "elasticsearch",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 32,
  "active_shards" : 32,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 3,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 91.42857142857143
}

# 查看集群成员列表
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -X GET 'http://localhost:9200/_cat/nodes?v'
ip        heap.percent ram.percent cpu load_1m load_5m load_15m node.role   master name
127.0.0.1           11          98   7    0.01    0.04     0.06 cdfhilmrstw *      lwz1

# 查看索引列表
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -X GET 'http://localhost:9200/_cat/indices?v'

# 创建索引(索引状态为yellow，这是因为该索引有一个副本)
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -X PUT  'http://localhost:9200/test-index'

# 修改副本数(单机模式下，副本改为0)
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -X PUT -H "content-type:application/json;charset=utf-8"   http://localhost:9200/test-index/_settings -d '{"number_of_replicas":0}'

# 查看索引mapping、setting和索引文档数
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" 'http://localhost:9200/test-index/_mapping?pretty'
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" 'http://localhost:9200/test-index/_settings?pretty'
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" 'http://localhost:9200/test-index/_count'

# 增加mapping
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -X POST -H "content-type:application/json;charset=utf-8"  'http://localhost:9200/test-index/_mapping' -d '{
      "properties" : {
        "content" : {
          "type" : "text"
        },
        "name" : {
          "type" : "keyword"
        }
      }
}'

# 新增数据
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -X POST -H "content-type:application/json;charset=utf-8"  'http://localhost:9200/test-index/_create/1' -d '{
    "name": "lwz",
    "content": "linux"
}'

# 查看索引内容
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -X GET 'http://localhost:9200/test-index/_search?pretty'
# 增加条件id为1
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -X GET 'http://localhost:9200/test-index/_doc/1?pretty'

# 清空索引内容
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -X POST 'http://localhost:9200/test-index/_delete_by_query?pretty' -H 'Content-Type: application/json' -d '{
  "query": {
    "match_all": {}
  }
}'

# 删除单条索引
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -XDELETE  'http://127.0.0.1:9200/index_name'

# 删除多条索引
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -XDELETE 'http://127.0.0.1:9200/index_01,index_02'

# 查看分片信息
[root@lwz1 ~]# curl -u elastic:"hK6mMKxrAqPzrcPXkIP9" -XGET 'http://127.0.0.1:9200/_cluster/allocation/explain?pretty'
```
