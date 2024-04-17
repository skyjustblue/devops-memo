# 私有镜像管理仓库harbor
Docker容器应用的开发和运行离不开可靠的镜像管理，虽然Docker官方也提供了公共的镜像仓库，但是从安全和效率等方面考虑，部署我们私有环境内的Registry也是非常必要的。Harbor是 由VMware公司开源的企业级的Docker Registry管理项目，它包括权限管理(RBAC)、LDAP、日志审核、管理界面、自我注册、镜像复制和中文支持等功能。

[harbor官方地址](https://goharbor.io)  
[github地址](https://github.com/goharbor/harbor)  

提前准备一个ca证书  
如果有自己的域名，可以到https://freessl.cn/ 申请免费的ssl证书

## 安装docker-compose
[安装docker-compose](./Docker-compose.md)

## 安装配置harbor
[下载地址](https://github.com/goharbor/harbor/releases)  

这里以v2.10.2为例  

```bash
# 将下载的包上传服务器并解压
tar zxf harbor-offline-installer-v2.10.2.tgz -C /opt/

# 备份配置文件
cd /opt/harbor
cp harbor.yml.tmpl harbor.yml
```
```bash
# 编辑配置文件
vim /opt/harbor/harbor.yml

# 修改hostname（域名或者ip）
hostname: 192.168.1.152
# 修改https证书
https:
  # https证书的路径
  certificate: /opt/harbor/cert/server.crt
  private_key: /opt/harbor/cert/server.key
# 修改密码
harbor_admin_password: 123123
# 修改数据存储路径
data_volume: /opt/harbor/data
```
```bash
# 安装harbor
./install.sh
```

## 启动停止harbor
```bash
cd /opt/harbor

# 启动harbor
docker-compose up -d

# 停止
docker-compose stop

# 查看
docker-compose ps

# 删除
docker-compose down
```

## 访问harbor
浏览器访问：https://192.168.1.152

默认用户名密码：admin/123123

## 操作镜像
```bash
# 拉取公共镜像
docker pull nginx

# 打标签
docker tag nginx 192.168.1.152/linyi/nginx:latest

# 登陆
docker login 192.168.1.152
## 输入用户密码

# 推送到harbor
docker push 192.168.1.152/linyi/nginx:latest
```

## 问题
x509: certificate signed by unknown authority  
（一般是私有证书或者免费证书才有的问题）
```bash
# 需要在客户端机器上（也就是你执行docker login的机器上）执行
echo -n | openssl s_client -showcerts -connect linyi.harbor.com:443 2>/dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' >> /etc/ssl/certs/ca-bundle.trust.crt

systemctl restart docker
```
