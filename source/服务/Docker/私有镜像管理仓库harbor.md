# 私有镜像管理仓库harbor
Docker容器应用的开发和运行离不开可靠的镜像管理，虽然Docker官方也提供了公共的镜像仓库，但是从安全和效率等方面考虑，部署我们私有环境内的Registry也是非常必要的。Harbor是 由VMware公司开源的企业级的Docker Registry管理项目，它包括权限管理(RBAC)、LDAP、日志审核、管理界面、自我注册、镜像复制和中文支持等功能。

[harbor官方地址](https://goharbor.io)  
[github地址](https://github.com/goharbor/harbor)  

## 安装docker-compose
[安装docker-compose](./Docker-compose.md)

## 安装配置harbor
[下载地址](https://github.com/goharbor/harbor/releases)  


这里以v2.10.2为例  
```bash
# 将下载的包上传服务器并解压
tar zxf harbor-offline-installer-v2.10.2.tgz -C /opt/

# 创建自签证书
mkdir -p /opt/harbor/cert
cd /opt/harbor/cert
openssl genrsa -out ca.key 4096
## 这里的CN=linyi.harbor.com写上habbor的域名,没有域名写上ip地址也可以
openssl req -x509 -new -nodes -sha512 -days 3650 \
 -subj "/C=CN/ST=Beijing/L=Beijing/O=example/OU=Personal/CN=linyi.harbor.com" -key ca.key -out ca.crt

# 备份配置文件
cd /opt/harbor
cp harbor.yml.tmpl harbor.yml
```
```bash
# 编辑配置文件
vim /opt/harbor/harbor.yml

# 修改hostname（域名或者ip）（ip：192.168.1.126 官方建议不用使用localhost or 127.0.0.1）
hostname: linyi.harbor.com
# 修改https证书
https:
  # https证书的路径
  certificate: /opt/harbor/cert/ca.crt
  private_key: /opt/harbor/cert/ca.key
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
浏览器访问：https://linyi.harbor.com

默认用户名密码：admin/123123

## 操作镜像
```bash
# 拉取公共镜像
docker pull nginx

# 打标签，标签格式为：镜像仓库域名/仓库名/镜像:tag
docker tag nginx linyi.harbor.com/linyi/nginx:latest

# 登陆
docker login linyi.harbor.com
## 输入用户密码
## 登陆成功后，账号密码被保存在 ~/.docker/config.json下
## 使用base64解密就能清晰的看到账号密码
echo "YWRtaW46SGFyYm9yMTIzNDU=" | base64 -d
## 为了安全,我们要及时退出登录
docker logout linyi.harbor.com

# 推送到harbor
docker push linyi.harbor.com/linyi/nginx:latest

# 下载镜像
docker pull linyi.harbor.com/linyi/nginx:latest
```

## 问题
x509: certificate signed by unknown authority  
（一般是私有证书或者免费证书才有的问题）
```bash
# 需要在客户端机器上（也就是你执行docker login的机器上）执行
echo -n | openssl s_client -showcerts -connect linyi.harbor.com:443 2>/dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' >> /etc/ssl/certs/ca-bundle.trust.crt

systemctl restart docker
```

## nginx反向代理harbor
[nginx安装参考](../Nginx/%E5%AE%89%E8%A3%85.md)  
nginx IP：192.168.1.11
```bash
# 配置nginx反向代理（先配置http，后面再通过certbot自动配置https）
vim /etc/nginx/conf.d/harbor.conf

server {
        listen  80;
        server_name linyi.harbor.com;

        location / {
                proxy_pass https://192.168.1.126:443;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_read_timeout 150;
        }
}

## 如果使用多台harbor做负载均衡，则使用如下配置
vim /etc/nginx/conf.d/harbor.conf

upstream harbor_server{				# 配置后端harbor
    ip_hash;						# 这里使用ip_hash,让同一个客户端请求同一个后端
    server 192.168.1.126:443;		# 指定harbor1的IP和端口,https端口是443
    server 192.168.1.127:4443;		# 指定harbor1的IP和端口,https端口是4443
}
server {
        listen  80;
        server_name linyi.harbor.com;

        location / {
                proxy_pass https://harbor_server;		# 反向代理到后端harbor
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_read_timeout 150;
        }
}


# 检查配置是否生效，重启nginx
nginx -t
nginx -s reload
```
### certbot配置https证书自动续期
[certbot安装配置参考](../Nginx/https%E4%B8%8ESSL.md)

### 客服端配置daemon.json连接harbor
[安装docker](./Docker%E5%AE%89%E8%A3%85.md)
```bash
# 在客户端指定nginx代理地址
vim /etc/docker/daemon.json

{
    "insecure-registries": ["harbor.jiuletech.com"]
}

# 重启docker
systemctl restart docker

# 登录harbor
docker login linyi.harbor.com

##如果登陆失败，可能需要将harbor.yml配置文件中的hostname修改为IP地址后，重装harbor
cd /opt/harbor/
docker-compose down
./install.sh
##再次从客户端登陆harbor
```