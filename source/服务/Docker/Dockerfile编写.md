# Dockerfile编写
什么是Dockerfile？是实现自定镜像的一种手段，通过编写Dockerfile，来编译成自己想要的镜像。

## Dockerfile 格式
```bash
# FROM 指定基于哪个基础镜像，例如：
FROM ubuntu:latest

# MAINTAINER  指定作者信息，例如：
MAINTAINER  linyi  linyi@test.com

# RUN 后面跟具体的命令，例如：
RUN apt update
RUN apt install -y curl
## 或
RUN ["apt","install","-y","curl" ]   ##这种写法偏复杂 

# CMD 用来指定容器启动时用到的命令，只能有一条，格式如下：
CMD ["executable", "param1", "param2"] 
CMD command param1 param2  
CMD ["param1", "param2"]
## CDM示例：
CMD ["/bin/bash", "/usr/local/nginx/sbin/nginx", "-c", "/usr/local/nginx/conf/nginx.conf"]

# EXPOSE 指定要映射的端口，格式：
EXPOSE <port> [<port>...]
## EXPOSE示例：
EXPOSE 22 80 8443  ##要暴露22，80，8443三个端口
## 说明：这个需要配合-P（大写）来工作，也就是说在启动容器时，需要加上-P，让它自动分配。如果想指定具体的端口，也可以使用-p（小写）来指定。

# ENV 为后续的RUN指令提供一个环境变量，我们也可以定义一些自定义的变量，例如
ENV MYSQL_version 5.7

# ADD 将本地的一个文件或目录拷贝到容器的某个目录里。 其中src为Dockerfile所在目录的相对路径，它也可以是一个url。例如： 
ADD conf/vhosts /usr/local/nginx/conf

# COPY 类似于ADD，将本地文件拷贝到容器里，不过它不支持URL，例如：
COPY 123.txt /data/456.txt

# ENTRYPOINT 格式类似CMD 
# 容器启动时要执行的命令，它和CMD很像，也是只有一条生效，如果写多个只有最后一条有效。
# 和CMD不同是： CMD 是可以被 docker run 指令覆盖的，而ENTRYPOINT不能覆盖。
## 比如，容器名字为linyi 我们在Dockerfile中指定如下CMD：
CMD ["/bin/echo", "test"]
### 假如启动容器的命令是  
docker run linyi
#### 则会输出 test
### 假如启动容器的命令是 
docker run -it linyi  /bin/bash  
#### 则什么都不会输出

## ENTRYPOINT不会被覆盖，而且会比CMD或者docker run指定的命令要靠前执行 
ENTRYPOINT ["echo", "test"]
### 假如启动容器的命令是
docker run -it linyi  123  
### 则会输出 test  123 ，这相当于要执行命令  echo test  123

# VOLUME 创建一个可以从本地主机或其他容器挂载的挂载点。
VOLUME ["/data"]

# USER指定RUN、CMD或者ENTRYPOINT运行时使用的用户
USER aming

# WORKDIR 为后续的RUN、CMD或者ENTRYPOINT指定工作目录
WORKDIR  /tmp/
```

## Dockerfile示例
定义一个ubuntu系统的镜像，在镜像中安装nginx、启动nginx服务。
```bash
# 创建工作目录
mkdir /data/dockerfile_test/
cd /data/dockerfile_test/
echo "lwz test docker" > index.html
vi  Dockerfile

# dockerfile内容
FROM ubuntu
MAINTAINER linyi linyi@test.com
RUN apt update
RUN apt install -y libpcre2-dev  net-tools gcc zlib1g-dev make
ADD http://nginx.org/download/nginx-1.23.2.tar.gz .
RUN tar zxvf nginx-1.23.2.tar.gz
RUN mkdir -p /usr/local/nginx
RUN cd nginx-1.23.2 && ./configure --prefix=/usr/local/nginx && make && make install
COPY index.html /usr/local/nginx/html/index.html
# COPY index2.html /usr/local/nginx/html/2.html
EXPOSE 80
ENTRYPOINT /usr/local/nginx/sbin/nginx -g "daemon off;"
## "daemon off;" 表示在前台运行，因为在docker中，后台运行服务会终止掉容器。
```
```bash
# 编译成镜像
docker build -t ubuntu_nginx:1.0 .
```
> 说明：  
> -t 后面跟镜像名字:tag， 这里的. 表示使用当前目录下的Dockerfile，并且工作目录也为当前目录，如果想使用其它目录下的Dockerfile，还可以使用-f选项来指定，例如：
> ```bash
> docker build -t ubuntu_nginx:1.0 -f  /data/docker/nginx.dkf  /tmp/
> # 这里/tmp/目录为工作目录，比如COPY文件的时候，到/tmp/下面去找
> ```

```bash
# 启动镜像
docker run -itd --name nginx -P  ubuntu_nginx:1.0

## 使用-P（大写P）随机映射一个宿主机端口到容器80，也可以使用-p（小p）指定具体端口，例如：
docker run -itd --name nginx_dockerfile -p 880:80 ubuntu_nginx:1.0

# 访问容器
[root@lwz1 dockerfile_test]# curl localhost:880
lwz test docker
```
