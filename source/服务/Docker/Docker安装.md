# Docker安装
在Rocky8上，可以先配置对应版本的yum仓库，然后使用yum工具安装Docker

```bash
# 先安装yum-utils工具
yum install -y yum-utils  

# 配置Docker官方的yum仓库
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# 查看Docker版本
yum list docker-ce --showduplicates | sort -r

# 安装指定版本Docker
yum install  docker-ce-20.10.9-3.el8
##或不指定版本，默认安装最新版
yum install docker-ce 

# 启动Docker
systemctl start docker
systemctl enable docker
```
