# pure-ftpd
相较传统ftp更为方便和安全的ftp服务器

## 服务端
1. 安装服务端
    ```
    yum install -y epel-release

    yum install -y pure-ftpd
    ```
2. 修改配置文件，将`# PureDB  @sysconfigdir@/pureftpd.pdb`取消注释并改为`PureDB   /etc/pure-ftpd/pureftpd.pdb`
    ```
    $ vim /etc/pure-ftpd/pure-ftpd.conf

    PureDB   /etc/pure-ftpd/pureftpd.pdb
    ```
    > PureDB 用于记录用户信息，默认情况下，它将使用纯文本文件来存储用户信息。
3. 启动服务
    ```
    systemctl start pure-ftpd
    ```
4. 创建共享目录
    ```
    mkdir /data/ftp -p
    ```
    > -p：递归创建目录
5. 创建本地用户，并修改共享目录所有者、所属组
    ```
    useradd pure-ftp
    chown -R pure-ftp:pure-ftp /data/ftp/
    ```
6. 创建pure-ftp虚拟用户和密码
    ```
    pure-pw useradd pftp1 -upure-ftp -d /data/ftp/
    ```
    生成数据库文件
    ```
    pure-pw mkdb
    ```
7. 创建用于测试的文件
    ```
    echo "hello world" > /data/ftp/1.txt
    ```

## 客户端
1. 连接ftp服务器
    ```
    lftp pftp1@192.168.1.152
    ```
    > 安装lftp：`yum install -y lftp`
2. 查看服务端共享的文件
    ```
    lftp pftp1@192.168.1.152:~> ls
    drwxr-xr-x    2 1002       pure-ftp         4096 Jan 10 11:52 .
    drwxr-xr-x    2 1002       pure-ftp         4096 Jan 10 11:52 ..
    -rw-r--r--    1 0          0                  12 Jan 10 17:11 1.txt
    ```
    > `!ls`查看本地目录下的文件

## lftp终端命令
- `put`：上传单个文件
- `mput`：上传多个文件

- `get`：下载单个文件
- `mget`：下载多个文件
- `pget`：多线程下载

- `exit` `quit`：退出lftp

| 远端命令 | 本地命令 | 说明 |
| :---: | :---: | :---: |
| ls | !ls | 查看目录下的文件 |
| cd | lcd | 切换目录 |
| pwd | lpwd | 查看当前所在路径 |


