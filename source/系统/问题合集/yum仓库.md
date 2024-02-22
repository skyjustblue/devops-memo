# yum

#### 错误：为仓库 ‘appstream‘ 下载元数据失败 : Cannot prepare internal mirrorlist: No URLs in mirrorlist

解决：
```bash
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

#### 同步仓库 'AppStream' 缓存失败，忽略这个 repo。
报错如下：
```
同步仓库 'AppStream' 缓存失败，忽略这个 repo。
同步仓库 'base' 缓存失败，忽略这个 repo。
同步仓库 'extras' 缓存失败，忽略这个 repo。
元数据缓存已建立。
```

解决：  
首先检查网络问题
```bash
# 检查网络
ping baidu.com
# 检查 yum 源
yum repolist
```

如果网络正常，则需要修改 yum 源配置文件，下面以改为阿里源为例
```bash
# 以下操作需要 root 权限
# 进入 repo 目录
cd /etc/yum.repos.d

# 建议备份原文件
cp CentOS-Base.repo{,.bak}
cp CentOS-AppStream.repo{,.bak}
cp CentOS-Extras.repo{,.bak}

vi CentOS-Base.repo
# 修改为以下内容
[BaseOS]
name=CentOS-$releasever - Base
baseurl=https://mirrors.aliyun.com/centos/$releasever/BaseOS/$basearch/os/
gpgcheck=1
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial


vi CentOS-AppStream.repo
# 修改内容
[AppStream]
name=CentOS-$releasever - AppStream
baseurl=https://mirrors.aliyun.com/centos/$releasever/AppStream/$basearch/os/
gpgcheck=1
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial

 
vi CentOS-Extras.repo
# 修改内容
[extras]
name=CentOS-$releasever - Extras
baseurl=https://mirrors.aliyun.com/centos/$releasever/BaseOS/$basearch/os/
gpgcheck=1
enabled=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial

# 清除缓存
yum clean all 

# 建立缓存
yum makecache
```