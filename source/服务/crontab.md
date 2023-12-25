# 用法及选项
```
crontab [-选项]
            选项：
                -u 用户名：指定某个用户执行cron
                -e：编辑crontab，即编辑某个用户的crontab
                -l：显示crontab，即显示某个用户的crontab
                -r：从/var/spool/cron中删除某个用户的crontab
```

# 配置文件
```
/etc/crontab
/var/spool/cron/root
/var/spool/

/var/log/cron       # 日志文件

$ cat /etc/crontab
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

# For details see man 4 crontabs

# Example of job definition:
# .---------------- minute (0 - 59) (分)
# |  .------------- hour (0 - 23) (时)
# |  |  .---------- day of month (1 - 31) (日)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ... (月)
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat (周、年)
# |  |  |  |  |
# *  *  *  *  * user-name  command to be executed
```

# 示例
```
# 进入编辑模式
$ crontab -e

# 每天00:00执行
0  0  *  *  *  sh /data/out_log_file.sh

# 每周一、周二、周三、周四、周五的10:00执行
0  10  *  *  1-5  sh /data/out_log_file.sh

# 每月1号、2号、3号、4号、5号的10:00执行
0  10  1,2,3,4,5  *  *  sh /data/out_log_file.sh

# 每一年1月1号、2号、3号、4号、5号的10:00执行
0  10  1,2,3,4,5  1  *  sh /data/out_log_file.sh

# 每隔1年1月1号、2号、3号、4号、5号的10:00执行
```
- 分 时 日 月 周  user command
- 分范围0-59，时范围0-23，日范围1-31，月范围1-12，周1-7
    - 星号（*）代表所有可能的值
    - 逗号（,）代表分隔
    - 中杠（-）代表一个范围
- 可用格式1-5表示一个范围1到5
- 可用格式1,2,3表示1或者2或者3
- 可用格式*/2表示被2整除的数字，比如小时，那就是每隔2小时

# 启动关闭服务
系统默认开启状态
```
$ systemctl status crond
$ systemctl start crond
$ systemctl stop crond
```
