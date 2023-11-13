# alias - 别名
alias通常为了方便将复杂的命令简化，提高我们的工作效率。

语法：
```
$ alias 简化后的别名=需要简化的命令
```
需要注意：
- 等号`=`两边不能有空格。
- 如果需要简化的命令中有特殊符号或者空格，需要使用单或双引号括起来。
- 单引号和双引号的区别：单引号中的变量会嵌入到别名中跟随使用；双引号中的变量会在别名定义时调用变量中的值在别名中。
    - 例如：
    ```
    [root@lwz1 ~]# alias dirA='echo path $PWD'
    [root@lwz1 ~]# alias dirA
    alias dirA='echo path $PWD'                 # 注意单引号中的变量执行后的变化

    [root@lwz1 ~]# alias dirB="echo path $PWD"
    [root@lwz1 ~]# alias dirB
    alias dirB='echo path /root'                # 注意双引号中的变量执行后的变化
    ```


## 用法：
```
查看所有别名
$ alias 

定义别名
$ alias dirA='echo path $PWD'       

取消定义别名
$ unalias dirA                      

慎用！ 取消所有别名定义
$ unalias -a
```

如果定义的别名和系统原本的命令冲突，三种解决方法：
```
绝对路径方法
$ /bin/vi test.sh
 
明确指定当前路径的方法
$ cd /bin
$ ./vi ~/test.sh
 
常用。使用反斜线的方法
$ \vi test.sh
```

## 别名永久生效
将别名的设置方案加入到用户的家目录（$HOME）下的`.alias`文件中（没有则创建），只能在创建的用户下使用，其他用户无法使用。
```
$ vi .alias                 # 加入如下内容
alias etc="cd /etc"         

$ vi .bashrc                # 加入如下内容
# Aliases
if [ -f ~/.alias ]; then
  . ~/.alias
fi
```
> 服务器重启后也能使用
