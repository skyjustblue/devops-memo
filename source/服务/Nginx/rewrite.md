# rewrite
域名跳转(重定向)、URL重写（伪静态）、动静分离（跳转域名，并接入CDN实现加速）
- 依赖PCRE库：安装`yum install -y pcre pcre-devel`
- 模块：ngx_http_rewrite_module

## if指令
- 语法：if (条件判断) { 具体的rewrite规则 }
- 条件判断：
    - 条件判断语句由Nginx内置变量、逻辑判断符号和目标字符串三部分组成。
    - 其中，内置变量是Nginx固定的非自定义的变量，如，$request_method, $request_uri等。
    - 逻辑判断符号，有=, !=, ~, ~*, !~, !~*
        - !表示相反的意思，~为匹配符号，它右侧为正则表达式，区分大小写，而~*为不区分大小写匹配。
    - 目标字符串可以是字符串，也可以是正则表达式，通常不用加引号，但表达式中有特殊符号时，比如空格、花括号、分号等，需要用单引号引起来。

### =示例：当请求的方法为POST时，直接返回405状态码
```bash
if ($request_method = POST)
{
    return 405;    # 在该示例中并未用到rewrite规则，if中支持用return指令。
}
```
实验：
```bash
[root@lwz1 vhost]# cat lwz.com
server {
	listen 80;
	server_name lwz.com;

	root /data/www/;
	index index.html index.php;

	if ($request_method = POST)
	{
		return 405;
	}
}

[root@lwz1 vhost]# curl -X POST lwz.com
\<html>
<head><title>405 Not Allowed</title></head>
<body>
<center><h1>405 Not Allowed</h1></center>
<hr><center>nginx/1.23.1</center>
</body>
</html>
```

### ~示例：user_agent带有MSIE字符的请求，直接返回403状态码
```bash
if ($http_user_agent ~ MSIE)
{
    return 403;
}
```
多个匹配条件：
```bash
if ($http_user_agent ~ "MSIE|firefox|spider")
{
    return 403;
}
```
实验：
```bash
[root@lwz1 vhost]# cat lwz.com
server {
	listen 80;
	server_name lwz.com;

	root /data/www/;
	index index.html index.php;

	if ($http_user_agent ~* curl)
	{
		return 403;
	}
}

[root@lwz1 vhost]# curl lwz.com
<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.23.1</center>
</body>
</html>
```

### !-f示例：当请求的文件不存在，将会执行下面的rewrite规则
```bash
if (!-f $request_filename)
{
    rewrite ^/(.*)$ /404.html break;
}
```
### ~*示例：不区分大小写的正则表达式匹配
```bash
# \d表示数字，{9,12}表示数字出现的次数是9到12次，如gid=123456789/就是符合条件的。
if ($request_uri ~* 'gid=\d{9,12}/')
{
    rewrite 
    ^/(.*)$ /index.php?gid=$1 last;
}
```

## break和last
两个指令用法相同，但含义不同，需要放到rewrite规则的末尾，用来控制重写后的链接是否继续被nginx配置执行(主要是rewrite、return指令)。

### 示例
```bash
[root@lwz1 vhost]# echo 333 >> /data/www/3.html
[root@lwz1 vhost]# echo 222 >> /data/www/2.html
[root@lwz1 vhost]# echo 111 >> /data/www/1.html
[root@lwz1 vhost]# cat lwz.com
server {
	listen 80;
	server_name lwz.com;

	root /data/www/;
	index index.html index.php;

	rewrite_log on;
	rewrite /1.html /2.html;
	rewrite /2.html /3.html;
}

[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com/1.html
333
```

### 示例：break和last在location {}外部，效果一致
```bash
# break
[root@lwz1 vhost]# cat lwz.com
server {
	listen 80;
	server_name lwz.com;

	root /data/www/;
	index index.html index.php;

	rewrite_log on;
	rewrite /1.html /2.html break;
	rewrite /2.html /3.html;
}
[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com/1.html
222

# last
[root@lwz1 vhost]# cat lwz.com
server {
	listen 80;
	server_name lwz.com;

	root /data/www/;
	index index.html index.php;

	rewrite_log on;
	rewrite /1.html /2.html last;
	rewrite /2.html /3.html;
}
[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com/1.html
222
```
当配置文件中有location时，它还会执行location{}段中的配置：
```bash
[root@lwz1 vhost]# !cat
cat lwz.com
server {
	listen 80;
	server_name lwz.com;

	root /data/www/;
	index index.html index.php;

	rewrite_log on;
	rewrite /1.html /2.html last;
	rewrite /2.html /3.html;

	location /2.html {
		return 403;
	}
}
[root@lwz1 vhost]# !curl
curl -x127.0.0.1:80 lwz.com/1.html
<html>
<head><title>403 Forbidden</title></head>
<body>
<center><h1>403 Forbidden</h1></center>
<hr><center>nginx/1.23.1</center>
</body>
</html>
```
### 示例：break和last在location {}内部
在location{}内部，遇到break，本location{}内以及后面的所有location{}内的所有指令都不再执行。
```bash
[root@lwz1 vhost]# !cat
cat lwz.com
server {
	listen 80;
	server_name lwz.com;

	root /data/www/;
	index index.html index.php;

	rewrite_log on;
	location / {
		rewrite /1.html /2.html;
		rewrite /2.html /3.html;
	}
	location /2.html {
		rewrite /2.html /a.html;
	}
	location /3.html {
		rewrite /3.html /b.html;
	}
}
[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com/1.html
b
```
> 不加break，会依次跳转到/2.html和/3.html，然后都跳转到/b.html

**添加break**，在location{}内部，遇到break，本location{}内以及后面的所有location{}内的所有指令都不再执行。
```bash
server {
        listen 80;
        server_name lwz.com;

        root /data/www/;
        index index.html index.php;

        rewrite_log on;
        location / {
                rewrite /1.html /2.html break;
                rewrite /2.html /3.html;
        }
        location /2.html {
                rewrite /2.html /a.html;
        }
        location /3.html {
                rewrite /3.html /b.html;
        }
}
[root@lwz1 vhost]# !curl
curl -x127.0.0.1:80 lwz.com/1.html
222
```

**添加last**，在location{}内部，遇到last，本location{}内后续指令不再执行，而重写后的url再次从头开始，从头到尾匹配一遍规则。最终会访问/a.html
```bash
server {
        listen 80;
        server_name lwz.com;

        root /data/www/;
        index index.html index.php;

        rewrite_log on;
        location / {
                rewrite /1.html /2.html last;
                rewrite /2.html /3.html;
        }
        location /2.html {
                rewrite /2.html /a.html;
        }
        location /3.html {
                rewrite /3.html /b.html;
        }
}
[root@lwz1 vhost]# !c
curl -x127.0.0.1:80 lwz.com/1.html
a
```
- 当rewrite规则在location{}外，break和last作用一样，遇到break或last后，其后续的rewrite/return语句不再执行。但后续有location{}的话，还会近一步执行location{}里面的语句,当然前提是请求必须要匹配该location。
- 当rewrite规则在location{}里，遇到break后，本location{}与其他location{}的所有rewrite/return规则都不再执行。
- 当rewrite规则在location{}里，遇到last后，本location{}里后续rewrite/return规则不执行，但重写后的url再次从头开始执行所有规则，哪个匹配执行哪个

## return指令
- 该指令一般用于对请求的客户端直接返回响应状态码。在该作用域内return后面的所有nginx配置都是无效的。
- 可以使用在server、location以及if配置中。
- 除了支持跟状态码，还可以跟字符串或者url链接。

### 返回状态码
```bash
# server中配置
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;
        return 403;
}

# 在if中配置
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;
        # 当uri请求.httppas和.bak结尾的文件时，返回405
        if ($request_uri ~ "\.httppas|\.bak")
        {
            return 405;
        }

# 在location中配置
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;
        # 访问/c.html时，返回404
        location /c.html
        {
           return 404;
        }
```

### 返回字符串
如果要想返回字符串，必须要加上状态码，否则会报错。

```bash
# 返回字符串
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;
        
        return 200 "lwz.com:200\n";
}
[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com
lwz.com:200

# 返回json数据
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;

        location ^~ /json
        {
            default_type application/json;
            return 200 '{"name":"josn","id":"100"}\n';
        }
}
[root@lwz1 vhost]# curl -x 127.0.0.1:80 lwz.com/json
{"name":"josn","id":"100"}
[root@lwz1 vhost]# curl -x 127.0.0.1:80 lwz.com/json -I
HTTP/1.1 200 OK
Server: nginx/1.23.1
Date: Mon, 18 Mar 2024 04:04:34 GMT
Content-Type: application/json
Content-Length: 27
Connection: keep-alive

# 返回变量
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;

        location ^~ /url
        {
            return 200 '$request_uri\n';
        }
}
[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com/url
/url

[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com/url -I
HTTP/1.1 200 OK
Server: nginx/1.23.1
Date: Mon, 18 Mar 2024 04:07:52 GMT
Content-Type: application/octet-stream
Content-Length: 5
Connection: keep-alive
```

### 返回url
注意：return后面的url必须是以http://或者https://开头的。
```bash
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;

        return http://lwz.com/a.html;
}
[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com -I
HTTP/1.1 302 Moved Temporarily
Server: nginx/1.23.1
Date: Mon, 18 Mar 2024 05:49:59 GMT
Content-Type: text/html
Content-Length: 145
Connection: keep-alive
Location: http://lwz.com/a.html
```

### 生产场景实战
背景：  
网站被黑了，凡是在百度点击到本网站的请求，全部都跳转到了一个赌博网站。  
通过nginx解决：  
```bash
if ($http_referer ~ 'baidu.com') 
{
    return 200 "<html><script>window.location.href='//$host$request_uri';</script></html>";
}

# 如果写成：
return http://$host$request_uri; 在浏览器中会提示“重定向的次数过多”。
```
测试：
```bash
[root@lwz1 vhost]# cat lwz.com
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;

	if ($http_referer ~ 'baidu.com')
	{
		return 200 "<html><script>window.location.href='//$host$request_uri';</script></html>\n";
	}
}
[root@lwz1 vhost]# curl -e "baidu.com" -x127.0.0.1:80 lwz.com/c.pac
<html><script>window.location.href='//lwz.com/c.pac';</script></html>
```

## rewrite规则
格式：`rewrite regex replacement [flag]`
- rewrite配置可以在server、location以及if配置段内生效

- regex是用于匹配URI的正则表达式，其不会匹配到$host（域名）

- replacement是目标跳转的URI，可以以http://或者https://开头，也可以省略掉host，直接写request_uri部分（即请求的链接）

- flag，用来设置rewrite对URI的处理行为，其中有break、last、rediect、permanent，其中break和last在前面已经介绍过，  
rediect和permanent的区别在于，前者为临时重定向(302)，而后者是永久重定向(301)，对于用户通过浏览器访问，这两者的效果是一致的。  
但是，对于搜索引擎蜘蛛爬虫来说就有区别了，使用301更有利于SEO。所以，建议replacemnet是以http://或者https://开头的flag使用permanent。

### 示例1
.*为正则表达式，用()括起来，在后面的URI中可以调用它，第一次出现的()用$1调用，第二次出现的()用$2调用，以此类推。
```bash
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;

        location /
        {
                rewrite /(.*) http://www.123.com/$1 permanent;
        }
}

[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com/1.html
<html>
<head><title>301 Moved Permanently</title></head>
<body>
<center><h1>301 Moved Permanently</h1></center>
<hr><center>nginx/1.23.1</center>
</body>
</html>

[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com/1.html -I
HTTP/1.1 301 Moved Permanently
Server: nginx/1.23.1
Date: Mon, 18 Mar 2024 06:17:37 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: http://www.123.com/1.html
```

### 示例2
在replacement中，支持变量，这里的$request_uri就是客户端请求的链接
```bash
[root@lwz1 vhost]# cat lwz.com
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;

	location /
	{
		rewrite /.* http:/123.com$request_uri permanent;
	}
}

[root@lwz1 vhost]# !cu
curl -x127.0.0.1:80 lwz.com/1.html -I
HTTP/1.1 301 Moved Permanently
Server: nginx/1.23.1
Date: Mon, 18 Mar 2024 06:20:33 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: http:/123.com/1.html
```

### 示例3
本例中的rewrite规则有问题，会造连续循环，最终会失败，解决该问题有两个方案。  
关于循环次数，经测试发现，curl 会循环50次，chrome会循环80次，IE会循环120次，firefox会循环20次。
```bash
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;

        rewrite /(.*) /data/www/123.com/$1 redirect;
}

[root@lwz1 vhost]# !cu
curl -x127.0.0.1:80 lwz.com/1.html -I
HTTP/1.1 302 Moved Temporarily
Server: nginx/1.23.1
Date: Mon, 18 Mar 2024 06:23:32 GMT
Content-Type: text/html
Content-Length: 145
Location: http://lwz.com/data/www/123.com/1.html
Connection: keep-alive

[root@lwz1 vhost]# curl -x127.0.0.1:80 lwz.com/1.html -L
curl: (47) Maximum (50) redirects followed
```
解决方案一：  
在rewrite中使用break，会避免循环。
```bash
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;
        rewrite /(.*) /123.com/$1 break;
}
[root@lwz1 vhosts]# !curl
curl lwz.com/2.html -I
HTTP/1.1 200 OK
Server: nginx/1.23.1
Date: Tue, 16 Aug 2022 06:14:31 GMT
Content-Type: text/html
Content-Length: 4
Last-Modified: Tue, 16 Aug 2022 06:14:04 GMT
Connection: keep-alive
ETag: "62fb35ac-4"
Accept-Ranges: bytes
```
解决方案二：  
加一个条件限制，也可以避免产生循环
```bash
server {
        listen 80;
        server_name lwz.com;
        root /data/www/;
        index index.html index.php;
         if ($request_uri !~ '^/123.com/') #当不是以123.com开头时，执行rewrite。
        {
            rewrite /(.*) /123.com/$1 redirect;
        }
}
[root@lwz1 vhosts]# curl return.com/2.html -L
222
```

## rewrite全局变量

|变量|说明|
|:---|:---|
|$args	| 请求中的参数，如www.123.com/1.php?a=1&b=2的$args就是a=1&b=2 |
|$content_length|	HTTP请求信息里的"Content-Length"|
|$conten_type	|HTTP请求信息里的"Content-Type"|
|$document_root	|nginx虚拟主机配置文件中的root参数对应的值|
|$document_uri|	当前请求中不包含指令的URI，如www.123.com/1.php?a=1&b=2的$document_uri就是1.php,不包含后面的参数|
|$host	|主机头，也就是域名|
|$http_user_agent	|客户端的详细信息，也就是浏览器的标识，用curl -A可以指定|
|$http_cookie|	客户端的cookie信息|
|$limit_rate	|如果nginx服务器使用limit_rate配置了显示网络速率，则会显示，如果没有设置， 则显示0|
|$remote_addr	|客户端的公网ip|
|$remote_port	|客户端的port|
|$remote_user	|如果nginx有配置认证，该变量代表客户端认证的用户名|
|$request_body_file	|做反向代理时发给后端服务器的本地资源的名称|
|$request_method	|请求资源的方式，GET/PUT/DELETE等|
|$request_filename	|当前请求的资源文件的路径名称，相当于是documentroot/document_uri的组合|
|$request_uri	|请求的链接，包括document_uri和args|
|$scheme	|请求的协议，如ftp,http,https|
|$server_protocol	|客户端请求资源使用的协议的版本，如HTTP/1.0，HTTP/1.1，HTTP/2.0等|
|$server_addr	|服务器IP地址|
|$server_name	|服务器的主机名|
|$server_port	|服务器的端口号|
|$uri	|和$document_uri相同|
|$http_referer	|客户端请求时的referer，通俗讲就是该请求是通过哪个链接跳过来的，用curl -e可以指定|

#### $args
```bash
[root@localhost vhosts]# cat 123.com.conf
    server {
        listen       80;
        server_name  123.com;
        root   /data/wwwroot/123.com;
        index  index.html index.php;
        rewrite_log on;
        return 200 $args;
   }
[root@localhost vhosts]# curl -x127.0.0.1:80 123.com/2.html?a=1
a=1
[root@localhost vhosts]# curl -x127.0.0.1:80 123.com/2.html?a=1\&b-2
a=1&b-2
```
#### $content_length
```bash
[root@localhost vhosts]# curl -x127.0.0.1:80 123.com/2.html?a=1\&b-2 -I
HTTP/1.1 200 OK
Server: nginx/1.23.1
Date: Thu, 18 Aug 2022 03:54:00 GMT
Content-Type: text/html
Content-Length: 7
Connection: keep-alive
```
#### $document_root
```bash
[root@localhost vhosts]# cat 123.com.conf
    server {
        listen       80;
        server_name  123.com;
        root   /data/wwwroot/123.com;
        index  index.html index.php;
        rewrite_log on;
        return 200 $document_root;
   }
[root@localhost vhosts]# curl -x127.0.0.1:80 123.com/2.html
/data/wwwroot/123.com
```
#### $http_user_agent
```bash
[root@localhost vhosts]# cat 123.com.conf
    server {
        listen       80;
        server_name  123.com;
        root   /data/wwwroot/123.com;
        index  index.html index.php;
        rewrite_log on;
        return 200 $http_user_agent;
   }
[root@localhost vhosts]# curl -A "fix" -x127.0.0.1:80 123.com/2.html
fix
```

## 实战
### 域名跳转(域名重定向)
#### 不带任何条件
```bash
server{
    listen 80;
    server_name www.aminglinux.com;
    rewrite /(.*) http://www.aming.com/$1 permanent;
    .......
    
}

# 测试
[root@localhost vhosts]# cat return.com.conf
    server {
        listen       80;
        server_name  return.com;
        root   /data/wwwroot/return.com;
        index  index.html index.php;
        rewrite /(.*) http://123.com/$1 permanent;
}
[root@localhost vhosts]# curl -x127.0.0.1:80 return.com/1.html -I
HTTP/1.1 301 Moved Permanently
Server: nginx/1.23.1
Date: Thu, 18 Aug 2022 04:43:25 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: http://123.com/1.html
```

#### 带条件
```bash
server{
    listen 80;
    server_name www.aminglinux.com aminglinux.com;
    if ($host != 'www.aminglinux.com')
    {
        rewrite /(.*) http://www.aminglinux.com/$1 permanent;
    }
    .......
    
}

# 测试
[root@localhost vhosts]# cat return.com.conf
    server {
        listen       80;
        server_name  return.com www.return.com;
        root   /data/wwwroot/return.com;
        index  index.html index.php;
        if ($host != return.com)
        {
        rewrite /(.*) http://123.com/$1 permanent;
        }
}
[root@localhost vhosts]# curl -x127.0.0.1:80 return.com -I
HTTP/1.1 403 Forbidden
Server: nginx/1.23.1
Date: Thu, 18 Aug 2022 04:48:31 GMT
Content-Type: text/html
Content-Length: 153
Connection: keep-alive

[root@localhost vhosts]# curl -x127.0.0.1:80 www.return.com -I
HTTP/1.1 301 Moved Permanently
Server: nginx/1.23.1
Date: Thu, 18 Aug 2022 04:48:38 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: http://123.com/
```

#### http跳转到https
```bash
server{
    listen 80;
    server_name www.aminglinux.com;
    rewrite /(.*) https://www.aminglinux.com/$1 permanent;
    .......
    
}

# 测试
[root@localhost vhosts]# cat return.com.conf
    server {
        listen       80;
        server_name  return.com www.return.com;
        root   /data/wwwroot/return.com;
        index  index.html index.php;
        rewrite /(.*) https://retrun.com/$1 permanent;
}

[root@localhost vhosts]# curl -x127.0.0.1:80 www.return.com -I
HTTP/1.1 301 Moved Permanently
Server: nginx/1.23.1
Date: Thu, 18 Aug 2022 04:51:39 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: https://retrun.com/
```
#### 域名访问二级目录
```bash
server{
    listen 80;
    server_name bbs.aminglinux.com;
    rewrite /(.*) http://www.aminglinux.com/bbs/$1 last;
    .......
    
}

# 测试
[root@localhost vhosts]# cat return.com.conf
    server {
        listen       80;
        server_name  return.com www.return.com;
        root   /data/wwwroot/return.com;
        index  index.html index.php;
        rewrite /(.*) http://retrun.com/123/$1 permanent;
}

[root@localhost vhosts]# curl -x127.0.0.1:80 www.return.com/1.html -I
HTTP/1.1 301 Moved Permanently
Server: nginx/1.23.1
Date: Thu, 18 Aug 2022 04:59:24 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: http://retrun.com/123/1.html
```

#### 静态请求分离
```bash
server{
    listen 80;
    server_name www.aminglinux.com;
    location ~* ^.+.(jpg|jpeg|gif|css|png|js)$
    {
        rewrite /(.*) http://img.aminglinux.com/$1 permanent;
    }

    .......
    
}
#或者：
server{
    listen 80;
    server_name www.aminglinux.com;
    if ( $uri ~* 'jpg|jpeg|gif|css|png|js$')
    {
        rewrite /(.*) http://img.aminglinux.com/$1 permanent;
    }

    .......
    
}

# 测试
[root@localhost vhosts]# !cat
cat return.com.conf
    server {
        listen       80;
        server_name  return.com www.return.com;
        root   /data/wwwroot/return.com;
        index  index.html index.php;
        if ($uri ~* 'jpg|css$')
        {
          rewrite /(.*) http://img.123.com/123/$1 permanent;
        }
}
[root@localhost vhosts]# curl -x127.0.0.1:80 www.return.com/1.html -I
HTTP/1.1 200 OK
Server: nginx/1.23.1
Date: Thu, 18 Aug 2022 05:08:56 GMT
Content-Type: text/html
Content-Length: 9
Last-Modified: Tue, 16 Aug 2022 05:33:08 GMT
Connection: keep-alive
ETag: "62fb2c14-9"
Accept-Ranges: bytes

[root@localhost vhosts]# curl -x127.0.0.1:80 www.return.com/1.html.jpg -I
HTTP/1.1 301 Moved Permanently
Server: nginx/1.23.1
Date: Thu, 18 Aug 2022 05:09:05 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: http://img.123.com/123/1.html.jpg

[root@localhost vhosts]# curl -x127.0.0.1:80 www.return.com/1.html.css -I
HTTP/1.1 301 Moved Permanently
Server: nginx/1.23.1
Date: Thu, 18 Aug 2022 05:09:10 GMT
Content-Type: text/html
Content-Length: 169
Connection: keep-alive
Location: http://img.123.com/123/1.html.css
```

### 防盗链
```bash
server{
    listen 80;
    server_name www.aminglinux.com;
    location ~* ^.+.(jpg|jpeg|gif|css|png|js|rar|zip|flv)$
    {
        valid_referers none blocked server_names *.aminglinux.com aminglinux.com *.aming.com aming.com;
        if ($invalid_referer)
        {
            rewrite /(.*) http://img.aminglinux.com/images/forbidden.png;
        }
    }

    .......
    
}
#说明：*这里是通配，跟正则里面的*不是一个意思，none指的是referer不存在的情况（curl -e 测试），
      blocked指的是referer头部的值被防火墙或者代理服务器删除或者伪装的情况，
      该情况下，referer头部的值不以http://或者https://开头（curl -e 后面跟的referer不以http://或者https://开头）。
#或者：
    location ~* ^.+.(jpg|jpeg|gif|css|png|js|rar|zip|flv)$
    {
        valid_referers none blocked server_names *.aminglinux.com *.aming.com aminglinux.com aming.com;
        if ($invalid_referer)
        {
            return 403;
        }
    }
```

### 伪静态
```bash
location /  {
    rewrite ^([^\.]*)/topic-(.+)\.html$ $1/portal.php?mod=topic&topic=$2 last;
    rewrite ^([^\.]*)/forum-(\w+)-([0-9]+)\.html$ $1/forum.php?mod=forumdisplay&fid=$2&page=$3 last;
    rewrite ^([^\.]*)/thread-([0-9]+)-([0-9]+)-([0-9]+)\.html$ $1/forum.php?mod=viewthread&tid=$2&extra=page%3D$4&page=$3 last;
    rewrite ^([^\.]*)/group-([0-9]+)-([0-9]+)\.html$ $1/forum.php?mod=group&fid=$2&page=$3 last;
    rewrite ^([^\.]*)/space-(username|uid)-(.+)\.html$ $1/home.php?mod=space&$2=$3 last;
    rewrite ^([^\.]*)/(fid|tid)-([0-9]+)\.html$ $1/index.php?action=$2&value=$3 last;
}
```
### rewrite多个条件的并且
```bash
location /{
    set $rule 0;
    if ($document_uri !~ '^/abc')
    {
        set $rule "${rule}1";
    }
    if ($http_user_agent ~* 'ie6|firefox')
    {
       set $rule "${rule}2";
    }
    if ($rule = "012")
    {
        rewrite /(.*) /abc/$1 redirect;
    }
}
```

--------------------------------------------

# location
## 安装第三方模块
echo-nginx-module
```bash
# 使用git安装模块
yum install -y git

# 克隆源码
cd /usr/local/src/
git clone https://github.com/openresty/echo-nginx-module.git
#或者下载源码上传到服务器
unzip echo-nginx-module-master.zip

# 进入nginx安装目录
cd nginx-1.23.1

# 查看nginx安装目录和已安装模块
nginx -V

# 加载第三方模块
./configure --prefix=/usr/local/nginx --with-http_ssl_module --add-module=/usr/local/src/echo-nginx-module

# 编译安装
make && make install

# 重启nginx
systemctl restart nginx

# 验证
server {
        listen 80;
        server_name lwz.com;
        root /data/www;
        index index.html index.php;

        location = "/10.html"
        {
                echo "10";
        }
}

# 请求
curl -x127.0.0.1:80 lwz.com/10.html
10
```

## location语法
nginx location语法规则：`location [=|~|~*|^~] /uri/ { … }`  
nginx的location匹配的变量是`$uri`  

|符号|说明|
|:--:|:--|
|=|表示精确匹配|
|^~	|表示uri以指定字符或字符串开头|
|~	|表示区分大小写的正则匹配|
|~*	|表示不区分大小写的正则匹配|
|/	|通用匹配，任何请求都会匹配到|

**优先级规则**  
= 高于 ^~ 高于 ~* 等于 ~ 高于 /

```bash
   location = "/12.jpg" { ... }
   如：
   www.aminglinux.com/12.jpg 匹配
   www.aminglinux.com/abc/12.jpg 不匹配
   
   location ^~ "/abc/" { ... }
   如：
   www.aminglinux.com/abc/123.html 匹配
   www.aminglinux.com/a/abc/123.jpg 不匹配
   
   location ~ "png" { ... }
   如：
   www.aminglinux.com/aaa/bbb/ccc/123.png 匹配
   www.aminglinux.com/aaa/png/123.html 匹配
   
   location ~* "png" { ... }
   如：
   www.aminglinux.com/aaa/bbb/ccc/123.PNG 匹配
   www.aminglinux.com/aaa/png/123.html 匹配
   
   location /admin/ { ... }
   如：
   www.aminglinux.com/admin/aaa/1.php 匹配
   www.aminglinux.com/123/admin/1.php 不匹配
```
> 小常识：   
> 有些资料上介绍location支持不匹配 !~，
如： `location !~ 'png'{ ... }`
这是错误的，location不支持 !~

> 如果有这样的需求，可以通过if来实现，
如： `if ($uri !~ 'png') { ... }`

> 注意：location优先级小于if
