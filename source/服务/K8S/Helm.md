# Helm
## Helm工具介绍
**了解Helm**  
Helm是kubernetes中查找、分享、构建应用的最佳方式。

Helm是一个Kubernetes应用的包管理工具，用来管理chart（一种预先配置好的安装包资源），有点类似于Ubuntu 的APT和CentOS/Rocky中的YUM。因此，helm的出现解决了k8s应用管理能力缺失的问题。

另外Helm也是dev和ops的桥梁，运维人员在使用Helm的时候，一方面不需要理解大量在Chart中的各种k8s元素，只需要配置少量的环境变量即可安装；另一方面，Helm也给初级运维人员提供了学习的机会，他们可以在Chart中学习并理解各种K8s元素，从而能够更快的掌握K8s。

官网地址： https://helm.sh/  
github地址：https://github.com/helm/helm/releases

**Helm核心概念**  
① Chart：Chart就是helm package，包含了一个k8s app应用运行起来的所有要素，比如service,deployment, configmap, serviceaccount, rbac, 等，这些要素都是以template文件的形式存在，再结合values文件，最终渲染出能够被k8s执行的yaml文件。

② Repository：仓库是charts的集合，方便进行分享和分发。我们可以将这个仓库添加到本地，然后从这些仓库里查找chart，并使用。

③ Hub: 不同的个人和组织提供的公共仓库（Repository）形成了分散和分布的Helm仓库，不利于查找，所以官方提供了Helm Hub，各公共仓库可以注册到Helm Hub中以方便集中查找，Helm Hub只是分布的仓库的集中展示中心。  
仓库注册到Helm Hub时，会将Chart清单文件向Helm Hub同步一份，这样可以在Helm Hub集中展示仓库列表和各仓库中的Chart列表。  
Chart包也就是tgz文件实际上存储在各仓库中。Helm Hub并不实际存储Chart包。Helm只是在查询Chart时和Helm Hub有交互，其它操作都是和仓库直接交互的。

④ Release：Release是Helm Chart在kubernetes的一个运行实例，这个release名字会体现在K8s里，其中service和deploy的名字跟这个release名字一致。

**Helm版本和Kubernetes版本要求**  
参考：https://helm.sh/zh/docs/topics/version_skew

## 安装Helm
说明：这里用的Kubernetes版本为1.25.4，考虑到后期会升级Kubernetes版本，所以helm版本为3.11

```bash
# 下载二进制包 
wget https://get.helm.sh/helm-v3.11.3-linux-amd64.tar.gz

# 解压并做软链
tar zxf helm-v3.11.3-linux-amd64.tar.gz  -C /opt/
mv /opt/linux-amd64/  /opt/helm
ln -s /opt/helm/helm  /bin/
```

## Helm常用命令
```bash
# 添加仓库，这样会把该仓库添加到本地
helm repo add bitnami https://charts.bitnami.com/bitnami  
helm repo add helm_sh https://charts.helm.sh/stable
helm repo add aliyun https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts

# 更新仓库列表到本地
helm repo update

# 查看仓库列表
helm repo list

# 在本地添加的仓库里搜索所有chart
helm search repo 

# 在本地的仓库里搜索mysql
helm search repo mysql

# 还可以从公共的hub里搜索chart，目的是找到合适的repo
helm search hub mysql  
##查看对应repo的url
helm search hub mysql  --list-repo-url 
##可以设置每一列的宽度，这样可以显示所有的描述信息 
helm search hub mysql  --max-col-width 100 

# 查看某个chart详细信息
helm show chart bitnami/mysql

# 查看某个chart values（这个values相当于是该cahrt的配置文件）
helm show values helm_sh/redis

# 安装chart (示例，安装nginx）
##先搜一下
helm search repo nginx 
##这个nginx-test就是release名字，同时也是service和deployment/statefulset以及pod前缀
helm install nginx-test bitnami/nginx 
##当然你也可以不去定义release name，让Helm帮忙定义，那么命令就要改为：
helm install bitnami/nginx --generate-name
###install过程中会自动生成缓存目录： ~/.cache/helm/repository/

# 安装完后，查看用helm安装过的chart
helm list -A
##-A会列出所有namespace里的release，不加-A只列default namespace里的release

# 卸载
helm uninstall nginx-test  

# 下载一个chart包（会下载一个tgz的压缩包）
helm pull bitnami/mysql 

# 利用本地的chart包，直接安装
tar zxf mysql-9.4.4.tgz
cd  mysql
helm install test-mysql .
```

## Helm工具实践
### 安装redis-cluster
先搭建一个NFS的SC（只需要SC，不需要pvc），具体步骤此文档不再提供，请参考前面文档。
```bash
# 下载redis-cluster的chart包(会下载一个目录下来)
helm pull bitnami/redis-cluster  --untar

# 修改values.yaml
cd redis-cluster
vi values.yaml 
##定义sc和密码
  storageClass: "nfs-client"
  redis:
    password: "123123"

# 安装
##注意，这是在chart的目录里，该目录下有values.yaml，后面的. 表示使用当前目录下的values.yaml
helm install redis-cluster .  

# 查看状态
helm status redis-cluster

# 测试
To get your password run:
    export REDIS_PASSWORD=$(kubectl get secret --namespace "default" redis-cluster -o jsonpath="{.data.redis-password}" | base64 -d)

You have deployed a Redis&reg; Cluster accessible only from within you Kubernetes Cluster.INFO: The Job to create the cluster will be created.To connect to your Redis&reg; cluster:

1. Run a Redis&reg; pod that you can use as a client:
kubectl run --namespace default redis-cluster-client --rm --tty -i --restart='Never' \
--env REDIS_PASSWORD=$REDIS_PASSWORD \
--image docker.io/bitnami/redis-cluster:7.0.5-debian-11-r19 -- bash

2. Connect using the Redis&reg; CLI:

redis-cli -c -h redis-cluster -a $REDIS_PASSWORD
```
### 应用的升级和回滚
```bash
# 安装好的应用，如果再次修改values.yaml（比如修改密码为456456)，则需要做升级处理
##注意，这是在chart的目录里，该目录下有values.yaml
helm upgrade  redis-cluster  .  

# 查看升级历史
helm history redis-cluster

# 回滚
helm rollback redis-cluster 1
```
## 自定义chart-内置对象
### Helm chart包目录结构
```bash
# 创建自定义chart模板
helm create my-template

# 查看目录结构
tree my-template

##说明：
* Chart.yaml：用于描述这个chart的基本信息，包括名字、描述信息、版本信息等。
* values.yaml：用于存储templates目录中模板文件中用到的变量信息，也就是说template中的模板文件引用的是values.yaml中的变量。
* templates：用于存放部署使用的yaml文件模板，这里面的yaml都是通过各种判断、流程控制、引用变量去调用values中设置的变量信息，最后完成部署。
    * deployment.yaml：deployment资源yaml文件。
    * ingress.yaml：ingress资源文件。
    * NOTES.txt：用于接收chart的帮助信息，helm install部署完成后展示给用户，也可以时候helm status列出信息。
    * _helpers.tpl：放置模板助手的地方，可以在整个chart中重复使用。
```
### helm chart模板
Helm最核心的就是模板，即模板化的K8s清单文件（如，deployment, service等），模板经过渲染后会被提交到K8s中，本质上就是Go语言的template模板，模板文件位于template/目录中。  
将K8s清单文件中可能经常变动的字段，通过指定一个变量，在安装的过程中该变量将被值value动态替换掉，这个过程就是模板的渲染。  
变量的值定义在values.yaml文件中，该文件中定义了变量的缺省值，但可以在helm install命令中配置新的值来覆盖缺省值。

#### 模板内置对象
##### Release对象
Release 对象描述了版本发布自身的一些信息。
- Release.Name：Release名字
- Release.Namespace：
Release所在命名空间
- Release.IsUpgrade：
如果当前操作是升级或回滚，则将其设置为true
- Release.IsInstall：
如果当前操作是安装，则设置为true
- Release.Revision：
此Release 的修订版本号
- Release.Service：
渲染此模板的服务，一般都是“Helm”

##### Values对象
Values 对象描述的是 values.yaml 文件中的内容，默认为空。使用 Value 对象可以获取到 values.yaml 文件中已定义的任何数值。  

Values对象的值有4个来源：
- chart包中的values.yaml文件；
- 父chart包的values.yaml文件；
- 通过helm install或者helm upgrade的-f 或者 --values参数传入的自定义的yaml文件（比如，helm install -f abc.yaml ）
- 通过--set传递单个参数（比如，helm install --set image=nginx:1.23.2）

优先级：--set  > -f  > 父chart里的values.yaml  > chart里的values.yaml

| Value 键值对 | 获取方式 |
| ------------ | ---------- |
| name: aaron | Values.name |
| info: name: aaron | Values.info.name |

##### Chart对象
Chart 对象用于获取 chart.yaml 文件中的内容
- Chart.Name：
获取Chart的名称
- Chart.Version：
获取Chart的版本
- Chart.apiVersion：
获取Chart的API版本
- Chart.description：
获取Chart的描述
- Chart.type：
获取Chart的类型
- Chart.keywords：
获取Chart的一组关键字

##### Capabilities对象
Capabilities 对象提供了关于 Kubernetes 集群相关的信息。
- Capabilities.APIVersions：
返回 Kubernetes 集群 API 版本信息集合
- Capabilities.APIVersions.Has $version：
用于检测指定的版本或资源在 Kubernetes 集群中是否可用，例如 batch/v1 或 apps/v1/Deployment
- Capabilities.KubeVersion ：
用于获取 Kubernetes 的版本号
-  Capabilities.KubeVersion.Version：
用于获取 Kubernetes 的版本号
- Capabilities.KubeVersion.Major：
Kubernetes 的主版本号
- Capabilities.KubeVersion.Minor：
Kubernetes 的小版本号

##### Template对象
Template 对象用于获取当前模板的信息
- Template.Name：
用于获取当前模板的名称和路径（例如：mychart/templates/mytemplate.yaml）
- Template.BasePath：
用于获取当前模板的路径（例如：mychart/templates）

##### Files对象
Files对象在chart中提供访问所有非特殊文件的对象。你不能使它访问template对象，只能访问其它文件。

- Files.Get：
通过文件名获取文件的方法
- Files.GetBytes：
用字节数组代替字符串获取文件内容的方法，常用于图片类的文件
- Files.Glob：
用给定的shell glob模式匹配文件名返回文件列表的方法
- Files.Lines：
逐行读取文件内容的方法
- Files.AsSecrets：
使用Base64编码字符串返回文件体的方法
- Files.AsConfig：
使用YAML格式返回文件体的方法

## Chart的values
**Values.yaml是Helm最重要的一个配置文件**
```bash
# 备份源文件
mv values.yaml  values.yaml.bak  

# 写一个自定义的值
cat > values.yaml <<EOF
myname: linyi
EOF

##调用上面自定义变量的方法为： 
{{ .Values.myname}}

# 在configmap.yaml里调用
##先备份一下template目录
cp -r templates/ templates.bak 
##删除掉所有模板文件
rm -rf templates/*  

cat > templates/configmap.yaml << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  myname: {{ .Values.myname }}
EOF

# 查看渲染效果
## 当前目录是在测试的chart里面，假定release名字为testrelease
helm template testrelease  .  
##但是，这个myname值是会被--set参数覆盖的，例如：
helm template testrelease . --set myname=linyi217

# 继续修改values.yaml内容
cat > values.yaml <<EOF
myname: linyi
service:
  type: ClusterIP
  port: 80
EOF
##要调用上面的type，需要引用 {{ Vlues.service.type}}

# 定义service.yaml
cat > templates/service.yaml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: testserivce
  labels:
    app: myapp
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
EOF

# 查看渲染效果：
helm template testrelease .
```
## Chart模板里的函数

函数列表： https://helm.sh/zh/docs/chart_template_guide/function_list/

A. quote函数：给对象加双引号，从而作为字符串使用
```bash
cat > templates/configmap.yaml << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  myname: {{ quote .Values.myname }}
EOF

# 渲染
helm template testrelease .
```
B. 管道+函数  
upper函数：小写变大写
```bash
cat > templates/service.yaml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: testserivce
  labels:
    app: myapp
spec:
  type: {{ .Values.service.type|upper|quote }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
EOF

# 渲染
helm template testrelease .
```
C. default函数：当对象值为空时，使用该函数定义的值
```bash
cat > templates/service.yaml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: testserivce
  labels:
    app: myapp
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port |default 8080 }}
      targetPort: http
      protocol: TCP
      name: http
EOF

# 渲染
helm template testrelease . --set service.port=null
```
D. indent函数： 缩进，例如indent 4，表示缩进4个字符
```bash
cat > templates/service.yaml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: testserivce
  labels:
    app: myapp
spec:
  type: {{ .Values.service.type|indent 8 }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
EOF

# 渲染
helm template testrelease . 
```
E. nindent函数： 换行并缩进
```bash
cat > templates/service.yaml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: testserivce
  labels:
    app: myapp
spec:
  type: {{ .Values.service.type|nindent 8 }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
EOF

# 渲染
helm template testrelease . 
```
## Chart模板流程控制if_with_range
### if
```bash
# 修改values.yaml
cat > values.yaml <<EOF
myname: linyi
service:
  type: ClusterIP
  port: 80
  myport: 8080
EOF

# 修改service.yaml
cat > templates/service.yaml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: testserivce
  labels:
    app: myapp
spec:
  type: {{ .Values.service.type }}
  ports:
    {{- if eq .Values.web "nginx" }}
    - port: {{ .Values.service.port }}
    {{- else }}
    - port: {{ .Values.service.myport }}
    {{- end }}
      targetPort: http
      protocol: TCP
      name: http
EOF

##说明：在if else end 左边加-，是为了去掉空行。{{- 表示删除左边的所有空格，直到非空格字符，而 -}}表示删除右边的所有空格。注意，换行符也是空格，当然还包括空格，TAB字符

# 渲染
helm template testrelease . --set web=nginx

  ports:
    - port: 80

# 如果不定义web变量的值，port为8080
helm template testrelease .

  ports:
    - port: 8080
```
### with 限定作用域
```bash
# with 的语法类似简单的 if:
{{ with PIPELINE }}
  # restricted scope
{{ end }}

# 没有用 with 的例子：
values.yaml：
env:
  host: localhost
  user: test
  hello: world

# deployment.yaml 的引用：
       {{- if .Values.env }}
        env:
        - name: host
          value: {{ .Values.env.host }}
        - name: user
          value: {{ .Values.env.user }}
        - name: hello
          value: {{ .Values.env.hello }}
        {{- end }}
```
上面的变量引用都需要从.Values开始， 有点繁琐。
```bash
# with 的例子：
## deployment.yaml 添加 with 以后：
       {{- with .Values.env }}
        env:
        - name: host
          value: {{ .host }}
        - name: user
          value: {{ .user }}
        - name: hello
          value: {{ .hello }}
        {{- end }}
## with 语句块里， 把当前范围定义在了.Values.env这个变量上了。

# 渲染后结果：
env:
 - name: host
   value: localhost
 - name: user
   value: test
 - name: hello
   value: world
```

### range  实现循环
```bash
# 在values.yaml 文件中添加上一个变量列表：
cat > values.yaml <<EOF
myname: linyi
service:
  type: ClusterIP
  port: 80
  myport: 8080
test:
  - 1
  - 2
  - 3
EOF

# 循环打印该列表：
cat > templates/configmap.yaml <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-configmap
data:
  myvalue: "Hello World"
  myname: {{ quote .Values.myname }}
  test: |
  {{- range .Values.test }}
    - {{ . }}   ##遍历循环打印所有元素
  {{- end }}
EOF

# 渲染
helm template testrelease .

  test: |
    - 1
    - 2
    - 3
```
## Chart模板中的变量
变量在模板中，使用变量的场合不多，但个别情况下不得不使用变量。

问题 1：获取数组键值
```bash
vim values.yaml
env:
  NAME: "gateway"
  JAVA_OPTS: "-Xmx1G"

vim deployment.yaml
...
env:
  {{- range $k, $v := .Values.env }}
    - name: {{ $k }}
      value: {{ $v | quote }}
   {{- end }}

# 结果如下
env:
  - name: JAVA_OPTS
    value: "-Xmx1G"
  - name: NAME
    value: "gateway"

## 上面在  range 循环中使用   $k 和 $v 两个变量来接收后面列表循环的键和值。
```
问题 2：with 中不能使用内置对象
```bash
# with 语句块内不能带 .Release.Name 对象，否则报错。我们可以将该对象赋值给一个变量可以来解决这个问题：
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deployment
spec:
  replicas: {{ .Values.replicas }}
  template:
metadata:
  labels:
    project: {{ .Values.label.project }}
    app: {{ quote .Values.label.app }}
   {{- with .Values.label }}
     project: {{ .project }}
     app: {{ .app }}
     release: {{ .Release.Name }}
    {{- end }}

# 上面会出错，但可以先定义变量，再调用它
{{- $releaseName := .Release.Name -}}
{{- with .Values.label }}
  project: {{ .project }}
  app: {{ .app }}
  release: {{ $releaseName }}
  
## 可以看到在with 语句上面增加了一句 {{- $releaseName:=.Release.Name- }}，其中$releaseName 就是后面的对象的一个引用变量，它的形式就是  $name，赋值操作使用:=，这样with 语句块内部的$releaseName 变量仍然指向的是.Release.Name
```
## Chart的命名模板
命名模板有时候也被称为部分或子模板。  
相对于 deployment.yaml 这种主模板，命名模板只是定义部分通用内容，然后在各个主模板中调用。  
templates目录下有个_helpers.tpl文件。公共的命名模板都放在这个文件里。

命名模板使用 define 来定义。  
```bash
# 如，这里先简单定义一个只包含字符串的模板，用作资源名称。
cat >  templates/_helpers.tpl <<EOF
{{/* 定义资源名称 */}}
{{ define "mytest.name" -}}
linyi217
{{- end }}
EOF

# 使用template引用
cat > templates/test.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ template "mytest.name" }}
  labels:
    app: {{ .Values.myname }}
EOF

# 渲染
helm template testrelease .
```
include用法：
```bash
cat >  templates/_helpers.tpl <<EOF
{{/* 定义资源名称 */}}
{{ define "mytest.name" -}}
linyi217
{{- end }}

{{/* 定义label */}}
{{- define "mytest.label" -}}
app: {{ .Release.Name }}
release: stable
env: qa
{{- end }}
EOF

# 在template的yaml文件里调用
cat > templates/test.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-{{ template "mytest.name" . }}
  labels:
    {{- include "mytest.label" . | nindent 4 }}
EOF

# 渲染
helm template testrelease .
```
## 自定义Chart实战
1.创建chart包
```bash
helm create  linyi217
```
2.自定义templates模板文件
```bash 
##删除掉默认的模板文件
cd  linyi217
rm -rf  templates/*

# 生成一个deployment模板
kubectl create deployment linyi217 --image=nginx:1.23.2 -o yaml --dry-run > templates/deployment.yaml

# 修改deployment.yaml
vi templates/deployment.yaml 
##改成如下内容
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: {{ .Values.appname }}                  #将values.yaml中的appname对应的变量值渲染在这里
  name: linyi217
spec:
  replicas: {{ .Values.replicas }}              #将values.yaml中的replicas对应的变量值渲染在这里
  selector:
    matchLabels:
      app: {{ .Values.appname }}                #标签可以和资源名称一样，因此也可以直接调用appname变量
  template:
    metadata:
      labels:
        app: {{ .Values.appname }}              #标签可以和资源名称一样，因此也可以直接调用appname变量
    spec:
      containers:
      - image: {{ .Values.image }}:{{ .Values.imageTag }}               #将values.yaml中的image、imageTag对应的变量值渲染在这里,表示镜像的版本号
        name: {{ .Values.appname }}                     #容器的名称也和资源的名称保持一致即可
        command: [ "/bin/sh","-c","/data/init.sh" ]
        ports:
        - name: web
          containerPort: 80
          protocol: TCP
        volumeMounts:
        - name: code
          mountPath: /data/code/linyi217
        - name: config
          mountPath: /data/nginx/conf/conf.d/
      volumes:  
        - name: config
          configMap:
            name: {{ .Values.appname }}-cm                              #confimap的名字也可以使用程序名称的变量加上-cm
        - name : code
          persistentVolumeClaim:
            claimName: {{ .Values.appname }}-pvc                #pvc的名字也可以使用程序名称的变量加上-pv
            readOnly: false    
```
```bash
# 编辑svc模板
vi templates/service.yaml ##写入如下内容
apiVersion: v1
kind: Service
metadata:
  labels:
    app: {{ .Values.appname }}                  #service要管理deployment的pod资源，因此这里的标签要和pod资源的标签对应上，直接调用appname这个变量
  name: {{ .Values.appname }}-svc               #service资源的名称，也可以直接调用appname这个变量，后面加一个-svc
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: {{ .Values.appname }}                  #标签选择器还是调用appname这个变量
  type: NodePort
```
```bash
# 编辑configmap模板
vi templates/configmap.yaml  ##写入如下内容
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Values.appname }}-cm                        #引入appname变量加上-cm作为cm资源的名称
data:
  test.linyi217.com.conf: |
    server {
      listen 80;
      server_name test.linyi217.com;
      location / {
        root /data/code/linyi217;
        index index.html;
      }
    }
```
```bash
编辑pv/pvc模板
vi templates/pv-pvc.yaml #内容如下
apiVersion: v1
kind:  PersistentVolume
metadata:
  name: {{ .Values.appname }}-pv                        #引入appname变量加上-pv作为pv资源的名称
  labels:
    pv: {{ .Values.appname }}-pv                        #标签也可以使用和pv名称一样的名字
spec:
  capacity:
    storage: 2Gi
  accessModes:
  - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  nfs:
    path: {{ .Values.nfsPath }}                         #这里会引入nfsPath变量的值
    server: {{ .Values.nfsServer }}                     #这里会引入nfsServer变量的值
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ .Values.appname }}-pvc                       #引入appname变量加上-pvc作为pvc资源的名称
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 2Gi
  selector:
    matchLabels:
      pv: {{ .Values.appname }}-pv                      #指定pv的标签
```
```bash
# 定义values.yaml 
vi  values.yaml #内容如下
appname: linyi217
replicas: 2
image: linyi217/helm-custom-chart  ##这是一个测试的镜像
imageTag: v0
nfsPath: /data/nfs/linyi217  ##这个目录需要提前创建好
nfsServer: 192.168.222.99
##注意：假定NFS服务器已经搭建好了
```
3.安装chart
```bash
helm  install  linyi217-release .

# 查看svc
kubectl get svc
```
4.到NFS服务器上创建一个测试页
```bash
echo "This is a test site." > /data/nfs/linyi217/index.html
```
浏览器访问：http://192.168.222.131:32745

## 使用Helm安装harbor
注意：如果你的harbor是之前docker-compose安装的，还需要额外做一个动作，让它支持chart
```bash
docker-compose stop
./install.sh --with-chartmuseum
```
Harbor的chartmuseum可以让Helm直接将chart包推送到harbor里，但是  
注意，harbor从2.8.0开始已经不支持chartmuseum了，而是改为了OCI ，鉴于新版本不太成熟和使用人太少，所以当前，我们安装2.6.2版本
```bash
# 查看历史版本
helm search repo harbor -l
# 下载harbor的chart包
## 16.1.0是chart的版本，而harbor版本为2.6.2
helm pull bitnami/harbor  --version 16.1.0 --untar

# 修改默认values.yaml
cd harbor
vi values.yaml  
##更改
storageClass: "nfs-client"  ##这个是提前搭建好的nfs的storageclass
###将所有"core.harbor.domain"替换为你自己的域名

# 安装
helm install myharbor --version 16.1.0 .

# 查看端口
kubectl get svc |grep harbor |grep LoadBalancer

# 查看密码
kubectl get secret --namespace default myharbor-core-envvars -o jsonpath="{.data.HARBOR_ADMIN_PASSWORD}" | base64 -d
```
浏览器登录： 
https://192.168.222.101:31666

## 将Chart推送到私有仓库harbor
```bash
# 安装helm-push插件
helm plugin install https://github.com/chartmuseum/helm-push

# 检查plugins列表
helm plugin list
NAME    VERSION DESCRIPTION
cm-push 0.10.1  Push chart package to ChartMuseum
```
**添加harbor地址**  
到harbor浏览器后台，添加新的项目 `chart_repo`
```bash
# helm添加harbor地址
helm repo add myharbor https://harbor.yuankeedu.com/chartrepo/chart_repo --username=admin --password=123123
##注意，如果出现x509的错误提示，执行
echo -n | openssl s_client -showcerts -connect harbor.yuankeedu.com:443 2>/dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' >> /etc/ssl/certs/ca-bundle.trust.crt

# 推送自定义chart包到harbor
##假如自定义chart目录：/root/helm_charts/linyi
cd /root/helm_charts
helm cm-push linyi/ myharbor

# 查看
helm repo update
helm search repo linyi

# 更新自定义chart
cd /root/helm_charts/linyi
vi Chart.yaml  ##更改版本号
vi values.yaml ##更改image版本号
## 升级本地release
helm upgrade linyi-release .
## 再次推送
cd ..
helm cm-push linyi/ myharbor

# 利用远程仓库安装新release
## 更新本地仓库
helm repo update

## 删除之前的release
cd /root/helm_charts/linyi
helm uninstall linyi-release

## 安装远程仓库
helm install linyi-2 myharbor/linyi
```