# 错误
`./autogen.sh` 安装时报错找不到pkg.m4

    Couldn't find pkg.m4 from pkg-config. Install the appropriate package for
    your distribution or set ACLOCAL_PATH to the directory containing pkg.m4.

使用`find`全局搜索

    root@jiule03:/usr/local/src/libxml2-v2.9.9# find / -name pkg.m4
    /usr/local/src/php-7.4.32/build/pkg.m4

copy到下列路径

    root@jiule03:/usr/local/src/libxml2-v2.9.9# cp /usr/local/share/aclocal/pkg.m4 /usr/share/aclocal/

再次执行`./autogen.sh`