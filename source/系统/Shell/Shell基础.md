# Shell基础

## history - 历史命令
`history`命令可以展示我们执行过的命令。执行过的命令，在正常退出终端的时候，都会报错在`/root/.bash_history`文件中。在退出终端前，执行过的命令在内存里面。

环境变量`$HISTSIZE`定义了`.bash_history`可以保存多少条历史命令。在`/etc/profile`文件里可以修改$HISTSIZE的值：
```
$ vim /etc/profile
HISTSIZE=1000           # 1000是默认值，修改数字即可
HISTTIMEFORMAT="%Y/%m/%d %H:%M:%S "     # 添加此条可显示命令执行时间

$ source /etc/profile   # 执行生效

$ chattr +a ~/.bash_history  # 防止被意外删除
```
终端操作：
- `history -c`：清除当前历史命令
- `!!`：执行上一条命令
- `!n`：执行`.bash_history`文件中的第n条命令
- `!word`：执行`.bash_history`文件中最近一次以word开头的命令
---
## 命令补全及别名
命令补全：终端输入命令或文件时，按`tab`键一下可以补全。按`tab`键两下可以列出当前关键字开头的所有命令或文件。

Centos7支持命令参数自动补全。需要安装`bash-completion`包：
```
$ yum install -y bash-completion
```

### 别名：
```
# 查看当前所有的别名
$ alias

# 新建别名。别名保存在/etc/profile.d/目录下和当前用户的.bashrc文件中。用户自定义的别名都保存在.bashrc文件中
$ alias lf='ls -a'      # 临时别名
$ vim ~/.bashrc         # 永久别名
alias lf='ls -a'

# 取消自定义别名
$ unalias lf
```
---
## 通配符
- `*`：匹配任意字符  
- `?`：匹配任意单个字符  
- `[]`：匹配任意个括号中的字符或数字，可以在中括号加入`0-9` `a-z` `A-Z`，例如：`ls [ao]*`表示以a和o开头的所有文件；`ls [1-3].txt`表示1.txt 2.txt 3.txt。
- `[!]`：不匹配中括号中的字符或数字，例如：`ls [!0-9]*`表示不以数字开头的文件  
- `{}`：匹配花括号中的任意个或范围的字符或数字，例如：
> ```
> $ ls {a,b,c}.txt        # 匹配a.txt b.txt c.txt
> $ ls {lwz,zc}.txt       # 匹配lwz.txt zc.txt
> $ touch {a..f}.txt      # 创建a到f这个范围的.txt文件
> ```

## 特殊符号
- `#`：在终端输入命令时，命令行提示符`#`后面的符号是当前用户是root用户，例如：`# ls`；在文件中，`#`代表注释。
- `\`：转义符；将特殊符号，转义成普通符号。
- `$`：在终端输入命令时，命令行提示符`$`后面的符号就是当前用户，例如：`$ ls`；也是shell中变量的前缀。
- `!$`：在正则表达式中表示行尾；在终端输入命令时，表示把上一条命令的参数作为标准输出，例如：
    - ```
        $ ls aa.txt
        aa.txt
        $ !ls
        ls aa.txt
        aa.txt
        或者
        $ ls !$
        ls aa.txt
        aa.txt
        ```
- `~`：在终端时表示用户的家目录；在正则表达式中表示匹配符。

## 输入、输出、重定向
- `0`：标准输入，从键盘输入
- `1`：标准输出，输出到终端
- `2`：标准错误，输出到终端
<br/>

- `>`：输出重定向，将命令执行的结果输出到文件中，如果文件存在，则覆盖，如果不存在，则创建。  
- `>>`：输出重定向，将命令执行的结果追加到文件中，如果文件存在，则追加，如果不存在，则创建。
- `2>`：标准错误，将命令执行过程中的错误信息覆盖到文件中，正确结果不输入。
- `2>>`：标准错误，将命令执行过程中的错误信息追加到文件中，正确结果不输入。
- `&>`：标准输出和标准错误都覆盖到文件中。
- `&>>`：标准输出和标准错误都追加到文件中。
- `<`：输入重定向，将文件中的内容作为命令的输入。

## 管道和任务控制
示例：`cat 11.txt | wc -l;cat 11.txt|grep 'pass'`
- `wc -l`：统计文件内容的行数或者文件的数量。
<br/>
管道：

- `|`：管道，将一个命令的输出作为另一个命令的输入。
- `;`：任务分隔，多个任务依次执行。

- `&&`：逻辑与，当第一个命令执行成功后，才执行第二个命令。
- `||`：逻辑或，当第一个命令执行失败后，才执行第二个命令。
<br>
任务控制：

- `&`：后台运行，将任务放到后台执行。在命令结尾加上`&`符号，如：`ping 127.0.0.1 &`，后台运行`ping`命令。
- `ctrl + z`：将任务放到后台，并暂停执行。（后台可以暂停多个任务）
- `jobs`：查看当前后台任务。
- `fg [id]`：将任务放到前台，并继续执行。
- `bg [id]`：将暂停的任务放到后台，并继续执行。
- `sleep`：延迟执行任务。默认以秒(s)为单位
    - 示例：`sleep 10s;ls`  # 10秒后执行`ls`命令
    - `s`为秒，`m`为分，`h`为小时，`d`为天
- `kill [id]`：结束任务，`id`为任务编号。


----
## Shell变量

### 变量类型
- 局部变量：局部变量在脚本或命令中定义，仅在当前shell实例中有效，其他shell启动的程序不能访问局部变量。
- 环境变量：所有的程序，包括shell启动的程序，都能访问环境变量，有些程序需要环境变量来保证其正常运行。必要的时候shell脚本也可以定义环境变量。
- shell变量：shell变量是由shell程序设置的特殊变量。shell变量中有一部分是环境变量，有一部分是局部变量，这些变量保证了shell的正常运行。

#### 环境变量配置文件
- `/etc/profile`：系统级，定义系统全局环境变量，该文件中定义的环境变量会在用户登陆时被加载。
- `/etc/bashrc`：系统级，但它仅对bash shell生效。当用户启动一个新交互式bash shell时，该文件会被读取，并设置bash shell特定的环境变量和执行一些系统级的初始化操作。
- `~/.bashrc`：用户级，用户的个人配置文件，该文件中的环境变量会在用户启动新的终端窗口时被加载。
- `~/.bash_profile`：用户级，该文件是每个用户的个人配置文件，该文件中定义的环境变量仅在该用户登陆时有效。

### 定义变量
```
name="lwz"      # 定义一个变量，变量名为name，变量值为lwz
```
> 注：变量名和等号之间不能有空格。同时，变量名的命名须遵循如下规则：
> - 命名只能使用英文字母，数字和下划线，首个字符不能以数字开头。
> - 中间不能有空格，可以使用下划线`_`。
> - 不能使用标点符号。
> - 不能使用bash里的关键字(可用`help`命令查看保留关键字)。

用语句给变量赋值：
```
# 将/etc目录下的文件
for file in `ls /etc`
或者
for file in $(ls /etc)
```

#### 单引号
```
$ myname='my name is lwz'
```  
单引号字符串的限制：
- 单引号里的任何字符都会原样输出，单引号字符串中的变量是无效的。
- 单引号字符串中不能出现单独一个的单引号（对单引号使用转义符后也不行），但可以成对出现，作为字符串拼接使用。

#### 双引号
```
$ name="lwz"
$ myname="my name is \"$name\" !"   # \为转义符，双引号中的双引号作用为拼接，转义后为普通双引号输出。
$ echo $myname
my name is "lwz" !
```
- 双引号里可以用变量。
- 双引号里可以出现转义字符。

#### 反引号
反引号` `` `，反引号中的内容会当做一个命令来执行，并且将执行结果作为变量的值。
```
# 将当前时间作为变量的值赋值给a。
$ a=`date`
$ echo $a
Wed Feb 26 16:37:15 CST 2019
```

#### 拼接字符串
```
$ name="lwz"

# 双引号拼接
$ myname="myname: my name is "$name" !"
$ myname1="myname1: my name is ${name} !"
$ echo $myname $myname1
myname: my name is lwz ! myname1: my name is lwz !

# 单引号拼接
$ myname2='myname2: my name is '$name' !'
$ myname3='myname3: my name is ${name} !'
$ echo $myname2 $myname3
myname2: my name is lwz ! myname3: my name is ${name} !
```

### 使用变量
变量名前面加上美元符号`$`即可。
```
$ echo $name
或者
$ echo ${name}
```
> 变量名外的花括号`{}`是可选的，建议加上，避免歧义，类似如下情况。
> ```
> $ echo ${name}123
> lwz123
> ```

### 只读变量
使用`readonly`命令将变量定义为只读变量，只读变量的值不能被更改。
```
# 将变量"name"设置成只读变量
$ readonly name
$ name="qqq"
-bash: name: readonly variable
```
> 注意：设置为只读变量，有可能无法删除。

### 删除变量
```
# 使用unset命令删除变量
$ unset name
```
---

## cut - 按列分割文本
cut命令将文本内容根据指定的规则分割成多列输出，默认分隔符为“TAB”。

### 语法
```
cut [选项参数] 文件
```
选项与参数：
- `-b`：以字节为单位进行分割。
- `-n`：与`-b`一起使用，表示禁止将字节分隔开来操作。
- `-c`：以字符为单位进行分割。
- `-d`：自定义分割字符。如果不加`-d`会默认字段分隔符为“TAB”；因此只能与`-f`一起使用。
- `-f`：以字段为单位进行分割；根据`-d`的分隔字符将一段信息分割成为数段，再用`-f`取出第几段的意思（列号，提取第几列）。
- `-s`：避免打印不包含分隔符的行。
- `--complement`：补足被选择的字节、字符或字段（反向选择的意思，或者说是补集）。
- `--output-delimiter`：更改输出分隔符；默认为输入分隔符。

### 示例
创建一个文本用于测试
```
[root@lwz ~]# cat rr.sh 
NO Name SubjectID Mark 备注
1  longshuai 001  56 不及格
2  gaoxiaofang  001 60 及格
3  zhangsan 001 50 不及格
4  lisi    001   80 及格
5  wangwu   001   90 及格
djakldj;lajd;sla
```

#### 按字段进行分隔
`rr.sh`文本一共有5列，筛选出第二列和第四列，使用空格作为分隔符。
```
[root@lwz ~]# cut -d" " -f2,4 rr.sh 
Name Mark
 001
 
 001
 
 
djakldj;lajd;sla
```
> 因为文本内容不规则，所以输出的内容是非预期的。

使用`tr`工具将重复的多个空格视为单个：
```
[root@lwz ~]# cat rr.sh | tr -s " " | cut -d" " -f2,4 
Name Mark
longshuai 56
gaoxiaofang 60
zhangsan 50
lisi 80
wangwu 90
djakldj;lajd;sla
```
最后一行完全没有分隔符的行也输出了，
使用`-s`来过滤这样的输出：
```
[root@lwz ~]# cat rr.sh | tr -s " " | cut -d" " -f2,4 -s
Name Mark
longshuai 56
gaoxiaofang 60
zhangsan 50
lisi 80
wangwu 90
```

使用`--complement`输出除了第二列和第四列以外的所有列：
```
[root@lwz ~]# cat rr.sh | tr -s " " | cut -d" " -f2,4 -s --complement
NO SubjectID 备注
1 001 不及格
2 001 及格
3 001 不及格
4 001 及格
5 001 及格
```
#### 按字节或字符分隔
英文和阿拉伯数字是单字节字符，中文是双字节或者是三字节。  
使用`-b`来筛选字节，`-c`筛选字符。  
> 注意：按字节或字符分隔时不能指定`-d`，因为`-d`是分隔字段的。

筛选第1个到第3个字节的内容：
```
[root@lwz ~]# cut -b1-3 rr.sh 
NO 
1 l
2 g
3 z
4 l
5 w
dja
```
筛选第3个到第6个字符的内容：
```
[root@lwz ~]# echo "今晚去哪喝!"|cut -c3-6
去哪喝!
```

#### `--output-delimiter`自定义分隔符
可以在多段分隔需要拼接时使用`--output-delimiter`来指定分隔符：
```
[root@lwz ~]# cut -b3-5,6-8 rr.sh   # 没有指定分隔符的拼接
 Name 
longsh
gaoxia
zhangs
lisi  
wangwu
akldj;

[root@lwz ~]# cut -b3-5,6-8 rr.sh --output-delimiter ":"    # 指定":"分隔拼接内容
 Na:me 
lon:gsh
gao:xia
zha:ngs
lis:i  
wan:gwu
akl:dj;
```

#### cut中的范围筛选
输出第3个字段往后的所有内容：
```
[root@lwz ~]# cut -d" " -f3- rr.sh -s
SubjectID Mark 备注
001  56 不及格
 001 60 及格
001 50 不及格
   001   80 及格
  001   90 及格
```

如果筛选的多段内容中有重复的，不会重复输出：
```
[root@lwz ~]# cut -d" " -f3-5,4-6 rr.sh -s      # 同`-f3-6`输出的内容一样。
SubjectID Mark 备注
001  56 不及格
 001 60 及格
001 50 不及格
   001
  001
```

在终端输入的分段顺序不会影响输出的顺序，cut只会按照文本内容的顺序输出：
```
[root@lwz ~]# cut -d" " -f4-6,2 rr.sh -s    # 两条命令输入的字段顺序不一样，但是输出内容还是一样的。
Name Mark 备注
longshuai  56 不及格
gaoxiaofang 001 60 及格
zhangsan 50 不及格
lisi   001
wangwu  001 

[root@lwz ~]# cut -d" " -f2,4-6 rr.sh -s
Name Mark 备注
longshuai  56 不及格
gaoxiaofang 001 60 及格
zhangsan 50 不及格
lisi   001
wangwu  001
```
-------------
## sort - 内容排序
sort命令将文件内容的每一行作为比较对象，通过将不同行进行互相比较，按照指定的排序规则进行排序输出，默认正序输出。

### 语法
```
sort [选项] 文件
```

常用选项：
- `-u`：不输出重复行。
- `-r`：倒叙输出。
- `-n`：按照数字排序。（特殊符号为0，所以输出在数字前面）
- `-o`：将排序后的结果输出到指定文件。
- `-t`：指定分隔符。（通常和-k一起使用）
- `-k`：指定排序的列。（通常和-t一起使用）

其他选项：
- `-f`：将小写字母转换为大写字母进行比较，即忽略大小写。
- `-b`：忽略每行前面开始处的空格字符。
- `-m`：合并已排序文件，而不是输出。
- `-M`：将每一行的月份用月份全称代替，例如JAN小于FEB，等等。
- `-c`：检查文件是否已经按照顺序排序，如果乱序，则输出第一个乱序的行的相关信息，最后返回1。
- `-C`：与-c选项类似，如果乱序，不输出内容，仅返回1。

### 示例
```
# 不加参数输出正序
[root@lwz ~]# sort seq.txt
!!@#
../
123
apple
apple:10:2.5
banana
banana:30:5.5
orange
orange:20:3.4
pear
pear
pear:90:2.3

# -r倒叙
[root@lwz ~]# sort -r seq.txt
pear:90:2.3
pear
pear
orange:20:3.4
orange
banana:30:5.5
banana
apple:10:2.5
apple
123
../
!!@#

# -u去重，-r倒叙，并将输出-o写入文件
[root@lwz ~]# sort -ur seq.txt -o seq2.txt
[root@lwz ~]# cat seq2.txt
pear:90:2.3
pear
orange:20:3.4
orange
banana:30:5.5
banana
apple:10:2.5
apple
123
../
!!@#

# -t指定分隔符为 : ，-k指定以:分隔后的第2列排序
[root@lwz ~]# sort -t: -k2 seq.txt
!!@#
../
123
apple
banana
orange
pear
pear
apple:10:2.5
orange:20:3.4
banana:30:5.5
pear:90:2.3
```
----
## wc - 内容统计
wc命令用于统计指定文件中的字节数、字数、行数，并将统计结果显示输出。

### 语法
```
wc [选项] [文件]
```
如果不加选项，默认统计文件中的总行数、总字数、总字节数，如果命令行中有文件名，则后面加上文件名依次输出，没有文件名则不输出文件名。  
如果不加文件名，会从标准输入读取内容（一般是结合其他命令一起使用）。  

选项：
- `-c`：统计字节数。
- `-l`：统计行数。
- `-m`：统计字符数。
- `-w`：统计字数。

### 示例
```
# 统计文件中的行数、字数、字节数，依次输出。
[root@lwz ~]# wc seq.txt
12 12 98 seq.txt

# 统计多个文件
[root@lwz ~]# wc -clw seq.txt seq2.txt      # 输出结果与不加选项相同
 12  12  98 seq.txt
 12  12  98 seq2.txt
 24  24 196 总用量

# -l统计行数（比较常用）
[root@lwz ~]# wc -l seq.txt
12 seq.txt

# 结合其他命令使用，统计ps -ef中的进程数
[root@lwz ~]# ps -ef | wc -l
92
```
-----------
## uniq - 内容去重
uniq命令用于输出或忽略文件中重复的行，一般与sort命令结合使用。

### 语法
```
uniq [选项] [文件]
```
选项：
- `-c`：在每列旁边显示该行重复出现的次数。
- `-d`：仅显示重复出现的行列，只显示一行。
- `-D`：显示所有重复的行，重复多少行就显示多少行。
- `-u`：仅显示出一次的行，不显示重复的行。
- `-i`：忽略大小写字符的不同。
- `-f [N]`：忽略第N列。
- `-s [N]`：忽略前面N个字符。
- `-w [N]`：忽略第N个字符后的内容。

### 示例
```
# 示例文本uniq.txt
[root@lwz ~]# cat uniq.txt
My name is Delav
My name is Delav
MY name is Delav
I'm learning Java
I'm learning Java
I'm learning Java
who am i
WHO am i
Python is so simple
My name is Delav
That's good
That's good
And studying Golang

# 不加选项默认输出去重后的内容
[root@lwz ~]# uniq uniq.txt
My name is Delav
MY name is Delav
I'm learning Java
who am i
WHO am i
Python is so simple
My name is Delav
That's good
And studying Golang

# 只显示重复的行-d，并显示重复次数-c
[root@lwz ~]# uniq -dc uniq.txt
      2 My name is Delav
      3 I'm learning Java
      2 That's good

# 忽略第2列（注意My和MY，忽略后就算重复的）
[root@lwz ~]# uniq -f2 uniq.txt
My name is Delav
I'm learning Java
who am i
Python is so simple
My name is Delav
That's good
And studying Golang

# 忽略前面3个字符（注意who和WHO会算作重复的，从第4个字符后就不算重复了）
[root@lwz ~]# uniq -s3 uniq.txt
My name is Delav
I'm learning Java
who am i
Python is so simple
My name is Delav
That's good
And studying Golang

# 结合sort命令一起使用（uniq只会把相邻的行算作重复，使用sort就能把不相邻的重复行排序到一起了）
[root@lwz ~]# sort uniq.txt | uniq -c
      1 And studying Golang
      3 I'm learning Java
      3 My name is Delav
      1 MY name is Delav
      1 Python is so simple
      2 That's good
      1 who am i
      1 WHO am i
```
--------
## tee - 重定向到标准输出和文件
- `tee`命令将一份标准输入分别重定向到标准输出`/dev/stdout`和指定的文件中，文件可以有多个。  
- `tee`命令与`>`、`>>`的区别是，`tee`命令会将输出重定向到文件的同时也输出在终端上。  
- 标准错误不会被`tee`读取到。

例：
```
[root@centos03 ~]# who | tee -a who.out
root     pts/3        2023-10-26 10:20 (192.168.1.110)

[root@centos03 ~]# cat who.out
root     pts/3        2023-10-26 10:20 (192.168.1.110)
```
- `tee tee.txt`：覆盖到文件，与`>`同理。
- `tee -a tee.txt`：追加到文件，与`>>`同理。
--------
## tr - 替换或删除字符
语法：`tr [参数] "被替换" "替换后"`

参数：
- `-d`：删除字符，即删除字符串中指定的字符。
- `-s`：把连续重复的字符以单独一个字符表示。
- `-c`：反选，即除了被指定的字符外其它的字符都处理。
- `-t`：删除所有属于第一字符集且不属于第二字符集的字符。

示例：
```
# 将结果小写转换为大写
[root@lwz ~]# who | tr "a-z" "A-Z" | tee test.txt
ROOT     TTY1         2023-10-24 16:02
ROOT     PTS/0        2023-10-24 16:07 (192.168.1.110)

# 将结果中的数字依次替换成字母，0=a、1=b、2=c，以此类推
[root@lwz ~]# echo '01222345' | tr '0-9' 'abcdefghijk' | tee test.txt
abcccdef

# 删除结果中数字以外的内容
[root@lwz ~]# echo '542asd99@#$' | tr -dc '0-9' | tee test.txt
54299

# 删除echo结果中数字以外的内容，并且去除结果中的重复数字
[root@lwz ~]# echo '542asd999999@#$' | tr -dc '0-9' | tr -s '0-9' | tee test.txt
5429
```

替换的范围表示：
```
[:digit:]       # 所有数字
 
[:lower:]       # 所有小写字符
 
[:upper:]       # 所有大写字符
 
[:graph:]       # 所有可打印字符，不包括空格
 
 
[:print:]       # 所有可打印字符，包括空格
 
[:punct:]       # 所有的标点字符
 
[:space:]       # 所有横向或者纵向的空白
 
[:xdigit:]      # 所有十六进制数字，包括0-9，a-f，A-F
```

-------

## split - 分割字符串
split命令用于将一个文件分隔成数个。  
该指定将大文件分割成较小的文件，在默认情况下将按照每1000行分割为一个小文件。

### 语法
```
split [选项] [被切割文件] [切割后的文件名]
```

选项：
- `-<行数>`：指定按多少行切割。
- `-b<字节>`：指定按多少字节切割。
- `-l<行数>`：也是指定按多少行切割。
- `-C<>`：与`-b`相似，但切割时会维持每行的完整性。
- `--version`：显示版本信息。
- `--help`：在线帮助。

示例：  
按每50行分割为一个文件：
```
[root@lwz 111]# split -50 11.txt    # 当不指定分割后的文件名时，文件名默认以 xa 开头

[root@lwz 111]# ls
11.txt  xaa  xab  xac  xad  xae  xaf  xag  xah  xai
```

按每1kb大小分割为一个文件，并且分割后的文件名以a1开头：
```
[root@lwz 111]# split -b1k 11.txt a1

[root@lwz 111]# ls
11.txt  a1aa  a1ab  a1ac  a1ad  a1ae  a1af  a1ag  a1ah  a1ai  a1aj  a1ak  a1al  a1am
```

将上一条命令执行的结果，按每5行存储到文件：
```
[root@lwz 111]# ps -ef | split -5

[root@lwz 111]# ls
11.txt  xab  xad  xaf  xah  xaj  xal  xan  xap  xar
xaa     xac  xae  xag  xai  xak  xam  xao  xaq  xas
```
