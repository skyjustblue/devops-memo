# ES单机版安装
修改服务器参数：
```bash
# 修改系统参数，调整文件打开数
cat >> /etc/security/limits.conf <<EOF
* soft nofile 102400
* hard nofile 102400
* soft nproc 10240
* hard nproc 10240
EOF

# 临时生效
ulimit -HSn 102400

# 修改内核参数
echo "vm.max_map_count=262144" >> /etc/sysctl.conf

# 使内核参数生效
sysctl -p
```

## yum安装ES(8.x版本)
[ES下载地址](https://www.elastic.co/cn/downloads/elasticsearch)  

[官方文档地址](https://www.elastic.co/guide/en/elasticsearch/reference/8.6/rpm.html#rpm-repo)

```bash
# 导入GPG Key
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch

# 创建yum仓库
cat > /etc/yum.repos.d/es.repo <<EOF
[elasticsearch]
name=Elasticsearch repository for 8.x packages
baseurl=https://artifacts.elastic.co/packages/8.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=0
autorefresh=1
type=rpm-md
EOF

# yum安装ES
yum install -y --enablerepo=elasticsearch elasticsearch
```
```bash
# 编辑配置文件，关闭ssl
vi  /etc/elasticsearch/elasticsearch.yml
##修改如下
xpack.security.http.ssl:
  enabled: false
##注释掉如下内容
# cluster.initial_master_nodes:["localhost.localdomain"]


# 启动ES
systemctl start elasticsearch
systemctl enable elasticsearch

# 查看端口(9200为RESTful接口访问端口，9300为集群通信端口)
netstat -lntp |grep java

# 重置密码
/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
##输出如下
Please confirm that you would like to continue [y/N] y
Password for the [elastic] user successfully reset.
New value: hK6mMKxrAqPzrcPXkIP9     # 新生成的密码

# 访问9200端口
curl -u elastic:'上一步生成的密码'  http://127.0.0.1:9200/
```

