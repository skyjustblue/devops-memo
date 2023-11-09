# logrotate - 日志分割
> * 分割逻辑：文件大小达到配置文件设置的指定大小后，会将文件改名为“`file.1` `file.2` `file.3` ...”以此类推，并新建一个`file`文件，我们把它叫做“转储”。
> * logrotate优点在于切割日志的同时，不丢失数据。
> * 系统自带的日志分割工具，配置文件在`/etc/logrotate.conf`和`/etc/logrotate.d/`目录下。

## 配置文件
```
$ cd /etc/logrotate.d/
$ vi test-logsplit
/var/log/test.log {
    daily
    rotate 7
    missingok
    notifempty
    minsize=1M
    maxsize=10M
    size=1M     # 设置文件切割临界点。
    compress
    delaycompress
    dateext
    dateformat .%Y-%m-%d
    create 0644 root root
    postrotate
        cat /dev/null > /var/log/test.log
    endscript
}
```

配置说明
* `/var/log/test.log`：需要切割的日志文件
* `daily`：日志文件每天切割一次
* `rotate 7`：保留7个切割后的日志文件
* `missingok`：如果日志文件丢失，不报错继续执行
* `notifempty`：如果日志文件为空文件，不进行切割
* `minsize=1M`：日志文件最小为1M
* `maxsize=10M`：日志文件最大为10M
* `size=1M`：日志文件大小为1M时进行切割
* `compress`：切割后日志文件进行压缩
* `delaycompress`：压缩的文件放到切割日志后，再进行压缩
* `dateext`：切割后的日志文件会加上时间后缀
* `dateformat .%Y-%m-%d`：时间后缀格式
* `create 0644 root root`：切割后的日志文件权限为0644，所有者root，所有组root
* `postrotate`：切割后执行的命令
* `endscript`：命令结束符

## 执行切割
```
$ logrotate -f /etc/logrotate.d/test-logsplit
```

## 配置cron定时切割
```
$ crontab -e
# 每天凌晨00点执行切割任务
0 0 * * * /usr/sbin/logrotate -f /etc/logrotate.d/test-logsplit
```
