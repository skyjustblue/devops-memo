# yum

#### 错误：为仓库 ‘appstream‘ 下载元数据失败 : Cannot prepare internal mirrorlist: No URLs in mirrorlist

解决：
```
mkdir /etc/yum.repos.d/bak

# 将源文件备份
mv /etc/yum.repos.d/CentOS-* /etc/yum.repos.d/bak

# 下载阿里云元数据文件
wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-vault-8.5.2111.repo

# 建立新元数据缓存
yum makecache
```
> 完成后重新下载需要的文件即可。       
> 参考：https://blog.csdn.net/qq_34670078/article/details/123543516