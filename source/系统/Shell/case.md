# case - 多分支匹配
`case ... esac`语句用于在多个分支中选择匹配，每个分支用`)`开始，当值匹配到某个分支时，执行该分支下的命令，命令可以有多个，需要换行隔开，直到所有命令执行完遇到`;;`结束。

## 语法格式
```
case 值 in
    分支1)
        命令1
        命令2
        ...
        命令n
        ;;
    分支2)
        命令1
        命令2
        ...
        命令n
        ;;
    *)
        命令1
        命令2
        ...
        命令n
        ;;
esac
```
> `*)`表示其他情况，可以省略，但`*`必须放在最后  
> 值可以为变量或常量，多个值之间用`|`分隔，如`1|2|3`表示值为1或2或3

## 示例
匹配数值
```
read -p "请输入一个数字:" aNum
case $aNum in
        1)
                echo '你选择了1'
                ;;
        2)
                echo '你选择了2'
                ;;
        3)
                echo '你选择了3'
                ;;
        4)
                echo '你选择了4'
                ;;
        *）
                echo '你没有输入1-4之间的数字'
                ;;
esac
```
匹配字符串
```
read -p "请输入一个字符串:" aStr
case $aStr in
        "hello")
                echo '你输入的是hello'
                ;;
        "world")
                echo '你输入的是world'
                ;;
        *)
                echo '你没有输入字符串'
                ;;
esac
```
> 双引号似乎可有可无?

匹配文件
```
read -p "请输入一个文件名:" aFile
case $aFile in
        *.sh)
                echo '你输入的是shell文件'
                ;;
        *.txt)
                echo '你输入的是txt文件'
		;;
        lwz.test)
                touch /root/case/$aFile
		;;
esac
```
