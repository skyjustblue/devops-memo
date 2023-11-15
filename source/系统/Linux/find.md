# find - 文件查找
## 简介
> find命令用来在指定路径下查找符合条件的文件。  

> find命令可以根据不同的条件来查找文件，比如按照文件名、文件大小、属主、属组、文件类型、时间等。同时还支持对搜索的结果进行其他命令的操作。

## 语法

    $ find [paths(查找的路径)] [parameter(参数)] [expressions(查找的条件)] [actions(处理操作)]
> find命令的路径可以指定一个或者多个，并默认在指定的路径下递归搜索，打印所有搜索的结果。

> 由于权限的问题，搜索时可能会报错，可以在命令的结尾加上`2>/dev/null`，避免显示大量无用信息。

## "查找"的选项和实例

### 根据文件名查找
选项：
* `-name "filename"`：区分大小写，支持使用glob，通配符 *、?、[]、[^]
* `-iname "filename"`：不区分字母大小写
* `-path "/path/name"`：匹配某个文件或目录的完整路径，而不仅仅是匹配文件名

实例

    # 查找/etc目录下所有以host开头的文件
    $ find /etc -name "host*"
    
    # 查找/etc目录下所有文件名刚好为4个字符的文件
    $ find /etc -name "????"

    # 查找/目录下所有以host开头的文件或目录，且该文件的父目录必须是/var/log
    $ find / -path "/var/log/host*"

### 根据文件类型查找

    选项：
    -type 类型
        f：普通文件
        d：目录
        l：符号链接文件
        s：套接字文件
        b：块设备文件
        c：字符设备文件
        p：管道文件
    
    实例
    # 查找/etc目录下所有以python开头的目录
    $ find /etc -type d -name "python*"

### 根据文件大小查找

    选项：
    -size [+ | -][文件大小][K|M|G(单位)]

    实例
    # 查找/etc目录下文件大小大于1G的文件
    $ find /etc -size +1G

    # 查找/etc目录下文件大小小于1M的文件
    $ find /etc -size -1M

### 根据时间戳查找

    选项：
    # 访问时间：最后一次文件又被读取过的时间点
    -atime [+ | -][时间戳]：
        +n：n天前被访问过的文件
        -n：n天内被访问过的文件
    -amin：以分钟为单位

    # 变更时间：最后一次文件有被变更过的时间点（如内容被修改，或权限等 metadata被修改）
    -ctime [+ | -][时间戳]：
        +n：n天前被修改过的文件
        -n：n天内被修改过的文件
    -cmin：以分钟为单位

    # 修改时间：最后一次文件内容有过修改的时间点
    -mtime [+ | -][时间戳]：
        +n：n天前被修改过的文件
        -n：n天内被修改过的文件
    -mmin：以分钟为单位

    实例
    # 查找/etc目录下访问时间在5天前，且变更时间在3天内的文件
    $ find /etc -atime +5 -ctime -3

    # 查找/etc目录下修改时间在5分钟内，且以".log"开头的文件
    $ find /etc -mmin -5 -name "*.log"

    # 查找/etc目录下访问时间在5天前，且修改时间在3天前，且文件大小在100M以下的文件
    $ find /etc -atime +5 -mtime +3 -size -100M

### 根据文件的所属权查找
    选项：
    -user 用户名：查找属主为指定用户的文件
    -group 组名：查找属组为指定组的文件
    
    -uid 用户id：查找属主为指定uid号的文件
    -gid 组id：查找属组为指定gid号的文件

    -nouser：查找没有属主的文件
    -nogroup：查找没有属组的文件

    实例
    # 查找/etc目录下属主为root,且属组为lwz的所有文件或目录
    $ find /etc -u root -a -group lwz

### 根据权限查找
    选项：
    -perm [+|-] Mode
        Mode：精确匹配权限
        +Mode：（u,g,o）对象的权限中只有有一位匹配Mode，即视为匹配
        -Mode：完全包含此mode时才匹配，每一类权限都必须同时拥有为其指定的权限标准

    实例
    # 查找/etc目录下权限为755的文件
    $ find /etc -perm 755

    # 查找/etc目录下必须所有类别用户都拥有写权限的文件
    $ find /etc -perm -222

    # 查找/etc目录下只要有一类用户拥有写权限的文件
    $ find /etc -perm +222

### 根据逻辑组合查找
    选项：
    -a：and（与）
    -o：or（或）
    -not：not（非）

    !A -a !B = !(A -o B)
    !A -o !B = !(A -a B)

    实例
    # 查找/etc目录下最近一周内其内容修改过，且属主不是root，且属组不是lwz的文件或目录
    $ find /etc -mtime -7 -not \( -user root -o -group lwz \)

    # 查找/etc目录下5分钟内或50分钟前被修改，且类型为文件的所有文件
    $ find /etc -mmin -5 -o -mmin +50 -type f
    $ find /etc '(' -mmin -5 -o -mmin +50 ')' -a -type f

## 对“查找”结果的处理动作
### 常用处理动作
* `-print`:默认的处理动作，将结果打印到标准输出
* `-ls`：类似于`ls -l`命令的显示方式。
* `-delete`：删除查找的结果
* `-fls /path/to/somefile`：查找到的文件长格式信息保存到指定文件。

* `-ok command {} \;`：
    * `-ok`：执行命令前，会交互式要求用户确认
    * `command`：要执行的命令
* `-exec command {} \;`：对查到的每个结果执行命令
    * 其中的大括号`{}`作为检索到的文件的占位符，用于引用查找到的结果。
    * 而分号`；`作为命令结束符，需要转义`\`。也可以用`+`号表示。
    * `-exec command {} \;` 等同于 `-exec command {} +`

实例：

    # 浏览所有1G以上大小的文件的详细信息
    $ find / -type f -size +1G -ls

    # 删除当前用户的home目录下所有的空目录
    $ find ~ -type d -empty -ok rm -rf {} \;
    或
    $ find ~ -type d -empty -delete
    # -empty：指定为空的文件或目录

    # 删除/var下空文件
    $ find /var -size 0 -type f -exec rm -rf {} \;

    # 删除海量文件，rm会很慢甚至卡死，find会快一些，或者安装rsync删除会更快。

## find结合xargs
注意：
> find传递查找到文件至后面指定的命令时，查找到所有符合条件的文件一次性传递给后面的指令有些命令不能接收过多参数，此时命令执行可能会失败，可以用xargs来规避此问题：
`find | xargs command`

xargs：
> （eXtended ARGuments）是给命令传递参数的一个过滤器，也是组合多个命令的一个工具。
> xargs可以将管道或标准输入（stdin）数据转换成命令行参数，也能够从文件的输出中读取数据。

### 常用实例
```
# 查找大于200M的文件，并显示具体大小。
$ find / -size +200M -type f 2>/dev/null |xargs du -sh

# 查找大于200M的文件，并显示详细信息
$ find / -size +200M -type f 2>/dev/null | xargs ls -l

# 查找系统中最大的10个文件
$ find / -type f -exec du -sh {} + 2>/dev/null | sort -rh | head -n 10

# 查找/etc下文件内包含"password"的文件
$ find /etc | xargs grep -ri "password"

# 遍历查找所有目录下的inode数量
$ for i in /*; do echo $i; find $i 2>/dev/null | wc -l; done

# 删除大于100M，时间在7天前的文件
$ find /test -size +100M -mtime +7 -delete
```
