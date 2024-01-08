# systemctl

#### systemctl没有访问权限
执行`systemctl status firewalld`报错：
Failed to get properties: Access denied

解决：    
重启系统或者执行`kill -TERM 1`  
（建议重启系统，`kill -TERM 1`可能会导致系统奔溃）
