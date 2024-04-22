# Docker安装
**Rocky8、7**  
在Rocky8上，可以先配置对应版本的yum仓库，然后使用yum工具安装Docker
```bash
# 先安装yum-utils工具
yum install -y yum-utils libseccomp-devel

# 配置Docker官方的yum仓库
yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# 查看Docker版本
yum list docker-ce --showduplicates | sort -r

# 安装指定版本Docker
yum install  docker-ce-20.10.9-3.el8 -y 
##或不指定版本，默认安装最新版
yum install docker-ce -y

# 启动Docker
systemctl start docker
systemctl enable docker
```
**ubuntu**  
```bash
# 卸载旧版本的Docker（如果有）
sudo apt-get remove docker docker-engine docker.io containerd runc

# 安装依赖项
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

# 添加Docker官方的GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# 设置Docker稳定版存储库
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
## 如果你需要安装特定版本的Docker而不是稳定版，可以将 stable 替换为 edge 或 test，并使用 VERSION 替换 XXX
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo apt-get install docker-ce=XXX

# 更新APT软件包索引
sudo apt-get update

# 查看可安装的docker版本
apt-cache madison docker-ce

# 安装特定版本的Docker20.10.0
sudo apt-get -y install docker-ce=5:20.10.0~3-0~ubuntu-focal docker-ce-cli=5:20.10.0~3-0~ubuntu-focal containerd.io

# 查看版本
sudo docker --version
```
