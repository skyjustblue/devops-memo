# for - 循环

## 语法
```
for 变量 in 值1 值2 值n
do
    命令1
    命令2
    命令n
done
```
终端写法
```
$ for 变量 in 值1 值2 值n; do 命令1; 命令2; 命令n; done
```

## 示例
### 循环一组数字
```
for i in 1 2 3 4 5; do
    echo "这是第 $i 次循环"
done
```
输出
```
这是第 1 次循环
这是第 2 次循环
这是第 3 次循环
这是第 4 次循环
这是第 5 次循环
```

### 循环输出字符串
```
for i in "This is a string";
do
    echo "$i"
done
```

### 遍历一个目录下的所有文件
```
#!/bin/bash

cd /root/for/100/

for a in `ls /root/for/100/`    # 将ls的结果赋值给$a
do
	[ -d $a ] && ls $a          # -d判断$a是否为目录，如果是则执行ls $a
	if [ -d $a ]
	then
		echo $a
		ls $a
	fi
done
```