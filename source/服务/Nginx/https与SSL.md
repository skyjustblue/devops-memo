# HTTPS与SSL配置

## SSL证书
免费ssl证书申请网站：
- [freessl.cn](https://freessl.cn/)
    - [freessl命令行工具部署证书](https://docs.certcloud.cn/docs/installation/auto/cmcli/)
- [Let’s Encrypt证书](https://certbot.eff.org/instructions?ws=nginx&os=centosrhel7)

## HTTPS配置
使用certbot工具自动生成Let’s Encrypt证书

## 配置解析
```
    server {
        listen       443 ssl;
        server_name  www.123.com;

        ssl_certificate ssl/server.crt;
        ssl_certificate_key ssl/server.key;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers ALL:!DH:!EXPORT:!RC4:+HIGH:+MEDIUM:!eNULL;
        ssl_prefer_server_ciphers on;

        error_log /usr/local/nginx/logs/123.error.log notice;
        access_log /usr/local/nginx/logs/123.access.log main;

        location / {
            root   /tmp/123.com;
            index  index.html index.htm;
        }
   }
```
- `443 ssl`：监听443端口，使用ssl协议
- `ssl_certificate`：证书文件路径
- `ssl_certificate_key`：私钥文件路径
- `ssl_protocols`：指定ssl协议版本，TLSv1和TLSv1.1有安全隐患，建议去掉
- `ssl_ciphers`：指定加密套件，多个套件用冒号分隔，`ALL`表示全部，`!`表示不启用，`+`表示将该套件排到最后
- `ssl_prefer_server_ciphers`：如果不指定默认为off，当为on时，在使用SSLv3和TLS协议时，服务器加密算法将优于客户端加密算法。
