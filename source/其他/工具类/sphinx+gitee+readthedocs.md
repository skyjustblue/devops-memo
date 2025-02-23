# 在线电子书sphinx + gitee + readthedocs

## 前提准备
1. gitee账号注册[官网：](https://gitee.com/)
注册时勾选.gitignore文件。

2. Read the Docs账号注册官网：<https://readthedocs.org/>

3. 安装VScode和Python3  
别人的链接：<https://blog.csdn.net/m0_37758063/article/details/128615786?ops_request_misc=&request_id=&biz_id=102&utm_term=%E5%AE%89%E8%A3%85vscode%E5%92%8Cpython&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-2-128615786.nonecase&spm=1018.2226.3001.4187>

## Sphinx创建文档
> Sphinx是一个基于Python的文档生成项目，开始是用来生成 Python 官方文档的工具，更多介绍可参考官网：https://www.sphinx.org.cn/ 。   
### 安装Sphinx   
Sphinx的GitHub地址：https://github.com/sphinx-doc/sphinx  

pip安装Sphinx 

    $ pip install -U sphinx  
### 创建文档
先将远程github仓库clone到本地，这个仓库是你要托管文档的仓库，如果没有就新建一个。   
clone到本地后，在项目根目录创建一个docs目录，cd进入docs目录，执行如下命令 

    $ sphinx-quickstart

```
Welcome to the Sphinx 4.2.0 quickstart utility.

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: .

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
> Separate source and build directories (y/n) [n]: y

The project name will occur in several places in the built documentation.
> Project name: 测试开发小记
> Author name(s): hiyongz
> Project release []: 0.1.0

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.
> Project language [en]: zh_CN

Creating file D:\pythonproj\devtest\source\conf.py.
Creating file D:\pythonproj\devtest\source\index.rst.
Creating file D:\pythonproj\devtest\Makefile.
Creating file D:\pythonproj\devtest\make.bat.

Finished: An initial directory structure has been created.

You should now populate your master file D:\pythonproj\devtest\source\index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.
```

上面的配置可以选择默认，稍后修改生成的conf.py配置文件即可.  
设置完成后，目录结构如下：  
```
│   make.bat
│   Makefile
│
├───build
└───source
    │   conf.py
    │   index.rst
    │
    ├───_static
    └───_templates
```
- build 存放编译后的文件
- source/_static 存放静态文件
- source/_templates 存放模板文件
- source/conf.py 项目配置文件，上面的配置可以在这里面修改
- source/index.rst 首页
### 编译
对rst文件进行编译生成HTML及相关静态文件：

    $ make html   
```
Running Sphinx v4.2.0
loading translations [zh_CN]... done
making output directory... done
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 1 source files that are out of date
updating environment: [new config] 1 added, 0 changed, 0 removed
reading sources... [100%] index
looking for now-outdated files... none found
pickling environment... done
checking consistency... done
preparing documents... done
writing output... [100%] index
generating indices... genindex done
writing additional pages... search done
copying static files... done
copying extra files... done
dumping search index in Chinese (code: zh)... done
dumping object inventory... done
build succeeded.
The HTML pages are in build\html.
Running Sphinx v4.2.0
loading translations [zh_CN]... done
making output directory... done
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 1 source files that are out of date
updating environment: [new config] 1 added, 0 changed, 0 removed
reading sources... [100%] index
looking for now-outdated files... none found
pickling environment... done
checking consistency... done
preparing documents... done
writing output... [100%] index
generating indices... genindex done
writing additional pages... search done
copying static files... done
copying extra files... done
dumping search index in Chinese (code: zh)... done
dumping object inventory... done
build succeeded.
The HTML pages are in build\html.
```

>index.rst文件内容会编译到_build/html目录下。   
### 配置主题
安装sphinx Read the Docs主题    

    $ pip install sphinx_rtd_theme  
>更多主题可到官网 https://sphinx-themes.org/ 查看。

配置`source/conf.py` 文件：   
```
html_theme = 'sphinx_rtd_theme' 
html_static_path = ['_static']
```

重新编译：  

    $ make html

## 本地http预览
### 安装autobuild工具
```
$ pip install -i https://pypi.tuna.tsinghua.edu.cn/simple sphinx-autobuild    
```
### 启动本地http页面
```
$ sphinx-autobuild source build/html
```

>*在本地浏览器输入127.0.0.1:8000在线预览*

## 配置markdown(.md)
>Sphinx默认使用 reStructuredText 标记语言，由于已经习惯使用markdown进行文档编辑，下面来配置markdown。
### 安装recommonmark插件
```
$ pip install recommonmark
```
### 安装支持markdown表格的插件
```
$ pip install sphinx_markdown_tables
```
>ReadTheDocs的python环境貌似没有sphinx_markdown_tables，在构建时可能报如下错误：

    ModuleNotFoundError: No module named 'sphinx_markdown_tables'
>解决方案是在docs目录下新建一个requirements.txt文件，写入如下内容：

    sphinx-markdown-tables==0.0.15
### 配置source/conf.py 文件
增加：

    extensions = ['recommonmark','sphinx_markdown_tables']

## 提交上传gitee
**.gitignore** 文件添加 __build/__ 目录，不需要上传这个目录。上传：

>在gitee创建仓库时勾选.gitignore文件，会在仓库自动生成。

    $ git add .    
    $ git commit -m "提交说明"
    $ git push -u origin master
## 关联Read the Docs
>关联Read the Docs，使其可以在线访问文档。

1. 浏览器访问 https://readthedocs.org/， 点击【我的项目】-> 【Import a Project】：

2. 选择手动导入

3. 点击下一步

4. 构建版本

5. 构建完成后，点击阅读文档


## 报错
### readthedocs构建问题
- conf.py语法错误:  
    修改项目仓库source/conf.py中错误语法，然后重新推送到gitee。

- readthedocs找不到`sphinx_markdown_tables`扩展。    
    在readthedocs仓库内创建一个`requirements.txt`文件，文件内添加缺失的扩展，重新推送到gitee，以此类推。

> 路径：`E:\read-the-docs\source\requirements.txt`  
> 文件内容：
> ```
> recommonmark
> sphinx-markdown-tables==0.0.17
> sphinx-rtd-theme==1.2.2
> ```
> 命令查看sphinx_markdown_tables版本号：
> ```
> $ pip show sphinx_markdown_tables    
> ```
> 其他缺什么扩展，在requirements.txt 中补上重新推送gitee，然后重新构建即可。

### readthedocs v1迁移v2问题
> 2023年八月尾，readthedocs v1将不再支持，需要迁移到v2。迁移过程很简单，但是坑很多。

以下是官方给的基础配置文档`.readthedocs.yaml`：
```
# .readthedocs.yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the version of Python and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

# Build documentation in the docs/ directory with Sphinx
sphinx:
  configuration: docs/conf.py

# We recommend specifying your dependencies to enable reproducible builds:
# https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html
# python:
#   install:
#   - requirements: docs/requirements.txt
```
1. `version: 2`，这是v2的配置文件，v1的配置文件是`readthedocs.yml`。
2. `build.os`，这是构建环境，是指readthedocs构建文档时所使用的操作系统，不是写我们的操作系统，默认即可。
3. `sphinx.configuration`，后面的路径应该是指git仓库存放项目的路径，readthedocs已经知道你的git仓库项目路径了，所以这里只需要从git项目仓库下开始写存放`conf.py`的路径。一般是`source/conf.py`
4. `python.install`，这个是安装依赖的，依赖的路径是git仓库下存放`requirements.txt`的路径。如果`requirements.txt`没有，则不需要写。路径还是只需要从git项目仓库下存放`requirements.txt`的路径开始写。

我就是在`python.install`这一步卡了半天，明明我的`requirements.txt`文件内有指定，但构建的时候一直报错找不到`recommonmark`模块。因为v1是不需要指定`requirements.txt`的路径的，v2需要指定，把注释去掉，然后把`requirements.txt`的路径写对就好了。

我的配置文件`.readthedocs.yaml`：
```
# .readthedocs.yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Optionally build your docs in additional formats such as PDF and ePub
formats: all

# Set the version of Python and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"


# Build documentation in the docs/ directory with Sphinx
sphinx:
  configuration: source/conf.py

# We recommend specifying your dependencies to enable reproducible builds:
# https://docs.readthedocs.io/en/stable/guides/reproducible-builds.html
python:
  install:
  - requirements: source/requirements.txt
```


