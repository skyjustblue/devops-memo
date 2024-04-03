# Nginx支持HTTP2
HTTP/2基于https的，需要先配置SSL  

依赖模块：--with-http_v2_module
```bash
[root@lwz1 nginx-1.23.1]# nginx -V
nginx version: nginx/1.23.1
built by gcc 8.5.0 20210514 (Red Hat 8.5.0-4) (GCC)
configure arguments: --prefix=/usr/local/nginx --add-module=/usr/local/src/echo-nginx-module

# 切换目录
cd /usr/local/src/nginx-1.23.1

# 查找相关模块
[root@lwz1 nginx-1.23.1]# ./configure --help|grep http_v2
  --with-http_v2_module              enable ngx_http_v2_module

# 安装依赖模块（把以编译的模块也加上）
./configure --prefix=/usr/local/nginx --add-module=/usr/local/src/echo-nginx-module --with-http_v2_module

make

# 备份源模块文件
systemctl stop nginx
mv /usr/local/nginx/sbin/nginx /usr/local/nginx/sbin/nginx.bak
cp objs/nginx /usr/local/nginx/sbin/
systemctl start nginx

[root@lwz1 nginx-1.23.1]# nginx -V
nginx version: nginx/1.23.1
built by gcc 8.5.0 20210514 (Red Hat 8.5.0-4) (GCC)
configure arguments: --prefix=/usr/local/nginx --add-module=/usr/local/src/echo-nginx-module --with-http_v2_module
```
```bash
# 配置文件
server {
    listen       443 ssl http2;    # 加上http2
    server_name  www.123.com;
    index index.html;
    root /data/wwwroot/server.com;

    ssl_certificate /etc/pki/ca_test/server/server.crt;
    ssl_certificate_key /etc/pki/ca_test/server/server.key;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ALL:!DH:!EXPORT:!RC4:+HIGH:+MEDIUM:!eNULL;
    ssl_prefer_server_ciphers on;
}
```