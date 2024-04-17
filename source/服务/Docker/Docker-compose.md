# Docker-compose
Docker compose可以方便我们快捷高效地管理容器的启动、停止、重启等操作，它类似于linux下的shell脚本，基于yaml语法，在该文件里我们可以描述应用的架构，比如用什么镜像、数据卷、网络模式、监听端口等信息。  
我们可以在一个compose文件中定义一个多容器的应用（比如wordpress），然后通过该compose来启动这个应用。 

## 安装docker-compose
[官网地址](https://github.com/docker/compose/releases)  

```bash
curl -L https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod a+x /usr/local/bin/docker-compose

# 测试并查看版本
docker-compose version
```

## 用docker-compose快速部署应用
```bash
# 编辑wordpress的compose yaml文件
vi docker-compose.yml

#写入如下内容
services:
   db:                   # 服务1：db
     image: mysql:5.7    # 使用镜像 mysql：5.7版本
     volumes:
       - db_data:/var/lib/mysql   # 数据持久化
     restart: always     # 容器服务宕机后总是重启
     environment:        # 环境配置
       MYSQL_ROOT_PASSWORD: 123123
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD: 123123

   wordpress:          # 服务2：wordpress
     depends_on:       # wordpress服务启动时依赖db服务，所以会自动先启动db服务
       - db
     image: wordpress:latest    # 使用镜像 wordpress：latest最新版
     ports:
       - "8000:80"          #端口映射8000:80
     restart: always
     environment:        # 环境配置
       WORDPRESS_DB_HOST: db:3306     # wordpress连接db的3306端口
       WORDPRESS_DB_USER: wordpress    # wordpress的数据库用户为wordpress
       WORDPRESS_DB_PASSWORD: 123123   # wordpress的数据库密码是123123
       WORDPRESS_DB_NAME: wordpress    # wordpress的数据库名字是wordpress
volumes:
    db_data: {}
```
```bash
# 启动应用，-d 表示后台启动
docker-compose up -d

# 查看应用状态
docker-compose ps

# 停止应用
docker-compose stop

# 删除应用
docker-compose down

# 重启应用
docker-compose restart

# 删除应用
docker-compose rm

# 进入应用
docker-compose exec wordpress bash

# 应用日志
docker-compose logs -f

# 应用日志，显示最后10条
docker-compose logs -f --tail 10
```
> 注意：  
> docker-compose命令需要在包含compose文件所在目录下执行，也就是通过compose创建容器时所在目录下，否则会提示找不到compose文件。  
