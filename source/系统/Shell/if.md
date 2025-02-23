# if - 逻辑判断

## if命令格式
### if

```
if 条件
then
    语句
fi
```

终端格式：
```
$ if 条件 ; then 语句 ; fi
```

### if else

```
if 条件
then
    语句1
else
    语句2
fi
```

终端格式：
```
$ if 条件 ; then 语句1 ; else 语句2 ; fi
```

### if elif else

```
if 条件1
then
    语句1
elif 条件2
then
    语句2
else
    语句3
fi
```
> elif可以有n个，格式为：`elif 条件n; then 语句n;`

终端格式：
```
$ if 条件1 ; then 语句1 ; elif 条件2 ; then 语句2 ; else 语句3 ; fi
```

## 条件中的用法

### 条件中的逻辑判断

| 操作符 | 描述 | 对应单词 |
| :------: | :------: | :------: |
| -gt | 大于 | greater than |
| -ge | 大于等于 | greater than or equal |
| -eq | 等于 | equality |
| -ne | 不等于 | inequality |
| -lt | 小于 | less than |
| -le | 小于等于 | less than or equal |

> 也可以用数学比较符表示：`<`小于，`>`大于，`==`等于，`!=`不等于，`>=`大于等于，`<=`小于等于

### 条件中的文件目录属性判断

- -f：判断是否是普通文件，且存在
- -d：判断是否是目录，且存在
- -e：判断文件或目录是否存在
- -r：判断文件是否可读
- -w：判断文件是否可写
- -x：判断文件是否可执行

### `&&`和`||`的用法 
&&表示逻辑与，即&&两边的条件同时成立即可
```
if 条件1 && 条件2
then
    语句1
fi
```

||表示逻辑或，即||两边的条件有一个成立即可
```
if 条件1 || 条件2
then
    语句1
fi
```

### 其他特殊用法
- `if [ -z "$a" ]`：判断变量a是否为空
- `if [ -n "$a" ]`：判断变量a是否不为空
- `if grep -q "a" $file`：判断文件中是否包含字符串a
- `if [ ! -e $file ]`：判断文件是否不存在

