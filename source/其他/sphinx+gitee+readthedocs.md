# 在线电子书sphinx + gitee + readthedocs

## 前提准备
1. gitee账号注册[官网：](https://gitee.com/)
注册时勾选.gitignore文件。

2. Read the Docs账号注册官网：<https://readthedocs.org/>

3. 安装VScode和Python3  
别人的链接：<https://blog.csdn.net/m0_37758063/article/details/128615786?ops_request_misc=&request_id=&biz_id=102&utm_term=%E5%AE%89%E8%A3%85vscode%E5%92%8Cpython&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-2-128615786.nonecase&spm=1018.2226.3001.4187>

## Sphinx创建文档
> Sphinx是一个基于Python的文档生成项目，开始是用来生成 Python 官方文档的工具，更多介绍可参考官网：https://www.sphinx.org.cn/ 。   
### 1. 安装Sphinx   
Sphinx的GitHub地址：https://github.com/sphinx-doc/sphinx  
pip安装Sphinx    
`$ pip install -U sphinx`   
2. ### 创建文档
先将远程github仓库clone到本地，这个仓库是你要托管文档的仓库，如果没有就新建一个。   
clone到本地后，在项目根目录创建一个docs目录，cd进入docs目录，执行如下命令   
`$ sphinx-quickstart`
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
3. ### 编译
对rst文件进行编译生成HTML及相关静态文件：   
`$ make html`   
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
4. ### 配置主题
安装sphinx Read the Docs主题    
`$ pip install sphinx_rtd_theme`    
>更多主题可到官网 https://sphinx-themes.org/ 查看。

配置`source/conf.py` 文件：   
```
html_theme = 'sphinx_rtd_theme' 
html_static_path = ['_static']
```

重新编译：  
`$ make html`

## 本地http预览
1. ### 安装autobuild工具
`$ pip install -i https://pypi.tuna.tsinghua.edu.cn/simple sphinx-autobuild`    

2. ### 启动本地http页面     
`$ sphinx-autobuild source build/html`
>在本地浏览器输入127.0.0.1:8000在线预览

## 配置markdown(.md)
>Sphinx默认使用 reStructuredText 标记语言，由于已经习惯使用markdown进行文档编辑，下面来配置markdown。
1. ### 安装recommonmark插件
`$ pip install recommonmark`

2. ### 安装支持markdown表格的插件
`$ pip install sphinx_markdown_tables`

>ReadTheDocs的python环境貌似没有sphinx_markdown_tables，在构建时可能报如下错误：

    ModuleNotFoundError: No module named 'sphinx_markdown_tables'
>解决方案是在docs目录下新建一个requirements.txt文件，写入如下内容：

    sphinx-markdown-tables==0.0.15
3. ### 配置source/conf.py 文件
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
- ### readthedocs构建问题
    - conf.py语法错误:  
    修改项目仓库source/conf.py中错误语法，然后重新推送到gitee。

    - readthedocs找不到‘sphinx_markdown_tables’  扩展。    
    在readthedocs仓库内创建一个requirements.txt文件，文件内添加缺失的扩展，重新推送到gitee。
```
$ pip show sphinx-rtd-theme    #查看sphinx-rtd-theme版本号，以此类推。
```
>其他缺什么扩展，在requirements.txt 中补上重新推送gitee，然后重新构建即可。




