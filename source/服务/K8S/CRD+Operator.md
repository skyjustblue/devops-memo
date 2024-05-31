# 自定义资源开发CRD+Operator

## API资源对象CustomResourceDefinition（CRD）
在Kubernetes中，像Pod、Service和Deployment这样的资源是由内置的资源类型如Pod、Service和Deployment表示的。而CustomResourceDefinition（CRD）允许你定义和创建自己的资源类型，以满足您的应用程序或基础设施需求。  

一旦定义了CRD，可以通过Kubernetes API服务器创建和管理自定义资源的实例，就像处理任何其他本机资源一样。这意味着您可以使用熟悉的Kubernetes工具如kubectl或Kubernetes控制器与管理您的自定义资源进行交互。  

CRD提供了一种扩展Kubernetes平台以适应特定要求的方式，并能够构建自定义的运算符或控制器来自动化管理自定义资源。运算符可以监视自定义资源的更改并相应地采取操作，例如提供额外的资源、扩展或执行自定义操作。  

CRD已成为扩展Kubernetes的流行机制，在Kubernetes生态系统中的各种项目和框架中广泛使用，如Prometheus、Istio和Knative。

```yaml
# 示例
cat > crd-example.yaml << EOF
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: myresources.example.com
spec:
  group: example.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          description: Define CronTab YAML Spec
          type: object
          properties:
            spec:
              type: object
              properties:
                name:
                  type: string
                age:
                  type: integer
  scope: Namespaced
  names:
    plural: myresources
    singular: myresource
    kind: MyResource        # 这里定义的Kind名称
    shortNames:
      - mr
EOF

## apiVersion：指定所使用的 CRD API 的版本，此示例使用了 apiextensions.k8s.io/v1 版本。
## kind：定义资源类型为 CustomResourceDefinition。
## metadata：定义元数据，其中 name 字段指定了 CRD 的名称为 myresources.example.com。
## spec：定义了 CRD 的规范。
## group：指定 CRD 所属的 API 组，此示例中为 example.com。
## versions：定义 CRD 的版本列表。
## name：指定版本的名称，此示例中为 v1。
## served：指定此版本是否由 API 服务器提供服务，设为 true 表示提供服务。
## storage：指定此版本是否持久化存储数据，设为 true 表示持久化存储。
## openAPIV3Schema： 指定自定义资源的 OpenAPI v3 架构定义
## type：定义类型
## properties：定义对象属性
## name/age：自定义具体属性的名字
## scope：指定资源的作用域，此示例中为 Namespaced，表示资源在命名空间级别进行管理。
## names：定义了资源的名称相关信息。
## plural：指定资源的复数形式名称，此示例中为 myresources。
## singular：指定资源的单数形式名称，此示例中为 myresource。
## kind：指定资源的类型名称，此示例中为 MyResource。
## shortNames：指定资源的缩略名称列表，此示例中只包含一个缩略名称 mr。
```
说明：  
和我们定义普通的资源对象比较类似，这里可以随意定义一个自定义的资源对象，但是在创建资源的时候，肯定不是任由我们随意去编写 YAML 文件的，当我们把上面的 CRD 文件提交给 Kubernetes 之后，Kubernetes 会对我们提交的声明文件进行校验，从定义可以看出 CRD 是基于 OpenAPI v3 schem 进行规范的。
```bash
# 应用
kubectl apply -f crd-example.yaml

# 查看crd
kubectl get crd

# 查看crd的详细信息
kubectl describe crd myresources.example.com

# 一旦创建完自定义的CRD，那么就会生成一个自定义的API
/apis/example.com/v1/namespaces/*/myresources/...
```
```yaml
# 创建自定义资源实例，基于前面CRD定义的资源
cat > myresource-instance.yaml <<EOF
apiVersion: example.com/v1
kind: MyResource   ##和上面CRD里相对应
metadata:
  name: myresource-instance
spec: ##以下两个key必须在CRD中有过定义
  name: example
  age: 25
EOF

# 应用
kubectl apply -f myresource-instance.yaml

# 查看MyResource
kubectl get MyResource  
## 或者用短名称
kubectl get mr
```
以上定义的CRD，仅仅是写入到了etcd中，并没有其它用处，要想让它有进一步作用，还得去定义Controller  
而Controller更多的是开发范畴的事情，咱们暂时先不涉及。

## Operator 

### Operator理论知识
#### Operator是什么
你可以理解成Operator就是CRD+自定义Controller的实践应用。

Kubernetes Operator由CoreOS公司开发，它是一种自定义控制器，它扩展了 Kubernetes API 的功能，用于管理和自动化应用程序、服务或资源的生命周期。Operator 可以将复杂的操作封装到 Kubernetes 中，以便在集群中创建、配置、部署和管理特定类型的应用程序或服务。

Operator 的核心思想是将应用程序的专业知识嵌入到自定义控制器中，以便控制器能够理解和管理特定类型的应用程序。这样一来，Operator 可以根据自定义资源的规范和状态，自动执行与应用程序相关的任务，如创建、更新、伸缩、备份和恢复等。Operator 还可以响应集群事件，自动修复故障和应用程序状态的健康性。  

通过使用 Operator，开发人员和管理员可以更轻松地在 Kubernetes 上管理复杂的应用程序和服务，减少手动操作的工作量，提高可靠性和可重复性。同时，Operator 的开放性设计使得可以创建适用于各种不同类型应用程序的自定义操作符，从数据库、消息队列到机器学习模型等各种类型的应用程序都可以通过 Operator 进行管理。
#### Operator用来做什么
使用 Operator 有很多理由。通常情况下，要么是开发团队为他们的产品创建 Operator，要么是 DevOps 团队希望对第三方软件管理进行自动化。无论哪种方式，都应该从确定 Operator 应该负责哪些东西开始。

最基本的 Operator 用于部署，使用 kubectl apply 就可以创建一个用于响应 API 资源的数据库，但这比内置的 Kubernetes 资源(如 StatefulSets 或 Deployments)好不了多少。复杂的 Operator 将提供更大的价值。如果你想要对数据库进行伸缩该怎么办？

如果是 StatefulSet，你可以执行 kubectl scale statefulset my-db --replicas 3，这样就可以得到 3 个实例。但如果这些实例需要不同的配置呢？是否需要指定一个实例为主实例，其他实例为副本？如果在添加新副本之前需要执行设置步骤，那该怎么办？在这种情况下，可以使用 Operator。

更高级的 Operator 可以处理其他一些特性，如响应负载的自动伸缩、备份和恢复、与 Prometheus 等度量系统的集成，甚至可以进行故障检测和自动调优。任何具有传统“运行手册”文档的操作都可以被自动化、测试和依赖，并自动做出响应。

被管理的系统甚至不需要部署在 Kubernetes 上也能从 Operator 中获益。例如，主要的云服务提供商（如 Amazon Web Services、微软 Azure 和谷歌云）提供 Kubenretes Operator 来管理其他云资源，如对象存储。用户可以通过配置 Kubernetes 应用程序的方式来配置云资源。运维团队可能对其他资源也采取同样的方法，使用 Operator 来管理任何东西——从第三方软件服务到硬件。

下面总结了一些常见的场景：
- 按需部署一个应用程序，并自动配置，比如Prometheus
- 需要备份和恢复应用程序的状态，如MySQL数据库
- 处理应用程序代码的升级以及相关更改，例如数据库架构或额外的配置设置
- 发布一个服务，要让不支持Kubernetes API的应用程序能够发现
- 模拟整个或部分集群中的故障以测试其弹性
- 在没有内部成员选举程序的情况下为分布式应用程序选择领导者

### Operator初次上手
需要有一点go的开发能力

目前主流的Operator开发框架有两个：kubebuilder和Operator-sdk， 两者实际上并没有本质的区别，它们的核心都是使用官方的 controller-tools 和 controller-runtime。不过细节上稍有不同，比如 kubebuilder 有着更为完善的测试与部署以及代码生成的脚手架等；而 operator-sdk 对 ansible operator 这类上层操作的支持更好一些。

下面基于kubebuilder，讲解如何开发Operator

#### 环境准备
Kubebuilder工作依赖go环境，所以需要安装go，生成环境应该单独准备一台机器来安装Kubebuilder。  
这里做实验在k8s3机器中演示  
```bash
# 安装go(Rocky8和Centos7都用yum安装，不过安装的版本有所不同)
yum install -y golang.x86_64

# 检测版本
go version

# 设置代理
go env -w GOPROXY=https://goproxy.cn,direct

# 查看GOPATH
go env GOPATH
##输出如下
/root/go

# 设置GOPATH（环境变量）
vim /etc/profile
##追加如下内容
export GOPATH=/root/go/

# 生效
source /etc/profile
```
[安装docker](../Docker/Docker%E5%AE%89%E8%A3%85.md)  

[安装kubectl](./%E5%8D%95%E6%9C%BA%E7%89%88%E5%AE%89%E8%A3%85.md)  
由于是在k8s3机器，已经安装过kubectl，如果没有安装请参考上面链接来安装。而默认k8s3机器是无法直接访问k8s集群的，需要将k8s1下面的/root/.kube目录拷贝到k8s3才可以
```bash
# 在k8s1执行
scp -r /root/.kube k8s3:/root/

# 在k8s3上测试
kubectl get node
```

安装kubebuilder
```bash
# 下载最新版（注意：最新版要求go的版本也比较新）
curl -k -L -o kubebuilder https://go.kubebuilder.io/dl/latest/$(go env GOOS)/$(go env GOARCH)
## 或者，下载指定版本
curl -k -L -o kubebuilder https://github.com/kubernetes-sigs/kubebuilder/releases/download/v3.10.0/kubebuilder_linux_amd64
# 赋予执行权限
chmod +x kubebuilder && mv kubebuilder /usr/local/bin/

# 测试
kubebuilder version
```
#### 创建Helloworld项目
**初始化项目**
```bash
export GOPATH=`go env GOPATH`
mkdir -p $GOPATH/src/helloworld 
cd $GOPATH/src/helloworld 
kubebuilder init --domain linyi.com

## 初始化完成后，目录结构是：
├── cmd
│   └── main.go
├── config
│   ├── default
│   │   ├── kustomization.yaml
│   │   ├── manager_auth_proxy_patch.yaml
│   │   └── manager_config_patch.yaml
│   ├── manager
│   │   ├── kustomization.yaml
│   │   └── manager.yaml
│   ├── prometheus
│   │   ├── kustomization.yaml
│   │   └── monitor.yaml
│   └── rbac
│       ├── auth_proxy_client_clusterrole.yaml
│       ├── auth_proxy_role_binding.yaml
│       ├── auth_proxy_role.yaml
│       ├── auth_proxy_service.yaml
│       ├── kustomization.yaml
│       ├── leader_election_role_binding.yaml
│       ├── leader_election_role.yaml
│       ├── role_binding.yaml
│       └── service_account.yaml
├── Dockerfile
├── go.mod
├── go.sum
├── hack
│   └── boilerplate.go.txt
├── Makefile
├── PROJECT
└── README.md
```
**创建API（CRD + Controller）**
```bash
# 先安装make，如果没有make会出问题
yum install -y make

# 创建API
kubebuilder create api --group webapp --version v1 --kind Guestbook
##打两次y
Create Resource [y/n]
y
Create Controller [y/n]
y
```
构建和部署CRD
```bash
# 这个过程会将CRD部署到k8s集群里
make install

# 我们可以查看CRD
kubectl get crd |grep linyi.com

# 我们可以通过下面命令查看该CRD对应的yaml
$GOPATH/src/helloworld/bin/kustomize build config/crd
```
**编辑Controller对应的源码，并编译**  
（如果是生产环境，此时就要去编辑Controller对应的go程序啦，由于我们是体验过程，所以只做简单改动
源码文件路径为：`$GOPATH/src/helloworld/internal/controller/guestbook_controller.go`）
```bash
vi $GOPATH/src/helloworld/internal/controller/guestbook_controller.go
## 改动1：增加一个依赖包fmt
import (
        "context"
        "fmt"       # 增加fmt

        "k8s.io/apimachinery/pkg/runtime"
        ctrl "sigs.k8s.io/controller-runtime"
        "sigs.k8s.io/controller-runtime/pkg/client"
        "sigs.k8s.io/controller-runtime/pkg/log"

        webappv1 "helloworld/api/v1"
)
## 改动2：找到// TODO(user): your logic here，在下面增加一行代码，用来打印堆栈信息
func (r *GuestbookReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
        _ = log.FromContext(ctx)

        // TODO(user): your logic here
        fmt.Println("Helloworld.")      # 增加此行

        return ctrl.Result{}, nil
}

# 改完后，执行
make run

# 这样就可以将该Controller运行起来了。会显示如下信息
test -s /root/go/src/helloworld/bin/controller-gen && /root/go/src/helloworld/bin/controller-gen --version | grep -q v0.11.3 || \
GOBIN=/root/go/src/helloworld/bin go install sigs.k8s.io/controller-tools/cmd/controller-gen@v0.11.3
/root/go/src/helloworld/bin/controller-gen rbac:roleName=manager-role crd webhook paths="./..." output:crd:artifacts:config=config/crd/bases
/root/go/src/helloworld/bin/controller-gen object:headerFile="hack/boilerplate.go.txt" paths="./..."
go fmt ./...
go vet ./...
go run ./cmd/main.go
2023-06-07T17:11:37+08:00       INFO    controller-runtime.metrics      Metrics server is starting to listen    {"addr": ":8080"}
2023-06-07T17:11:37+08:00       INFO    setup   starting manager
2023-06-07T17:11:37+08:00       INFO    Starting server {"path": "/metrics", "kind": "metrics", "addr": "[::]:8080"}
2023-06-07T17:11:37+08:00       INFO    Starting server {"kind": "health probe", "addr": "[::]:8081"}
2023-06-07T17:11:37+08:00       INFO    Starting EventSource    {"controller": "guestbook", "controllerGroup": "webapp.aminglinux.com", "controllerKind": "Guestbook", "source": "kind source: *v1.Guestbook"}
2023-06-07T17:11:37+08:00       INFO    Starting Controller     {"controller": "guestbook", "controllerGroup": "webapp.aminglinux.com", "controllerKind": "Guestbook"}
2023-06-07T17:11:38+08:00       INFO    Starting workers        {"controller": "guestbook", "controllerGroup": "webapp.aminglinux.com", "controllerKind": "Guestbook", "worker count": 1}
## 说明：不要按ctrc c中断，此时需要我们到k8s那边去
```
**到k8s创建Guestbook资源的实例**  

现在kubernetes已经部署了Guestbook类型的CRD，而且对应的controller也已正在运行中，可以尝试创建Guestbook类型的实例了(相当于有了pod的定义后，才可以创建pod)；

kubebuilder已经自动创建了一个类型的部署文件：`$GOPATH/src/helloworld/config/samples/webapp_v1_guestbook.yaml` ，内容如下，很简单，接下来咱们就用这个文件来创建Guestbook实例：
```bash
cat > guestbook.yaml <<EOF
apiVersion: webapp.aminglinux.com/v1
kind: Guestbook
metadata:
  labels:
    app.kubernetes.io/name: guestbook
    app.kubernetes.io/instance: guestbook-sample
    app.kubernetes.io/part-of: helloworld
    app.kubernetes.io/managed-by: kustomize
    app.kubernetes.io/created-by: helloworld
  name: guestbook-sample
spec:
  # TODO(user): Add fields here
  foo: bar
EOF

# 应用此yaml
kubectl apply -f guestbook.yaml

# 回到aminglinux03的终端，可以看到多了一行输出
Helloworld.
```
**将Controller制作成镜像，并上传到远程仓库**  
首先需要有一个私有镜像仓库，用来存储编译好的镜像。如果有harbor直接使用harbor最好，如果没有，就是用docker的镜像仓库hub.docker.com，假设你已经有账号了。  

```bash
# 在编译镜像之前还需要登录到docker的镜像仓库
docker login  https://hub.docker.com
## 或者登陆harbor
docker login https://harbor.yuankeedu.com

# 给Dockerfile里增加GOPROXY设置
vi  Dockerfile 
##在go mod download上面增加一行
RUN go env -w GOPROXY=https://goproxy.cn

# 编译镜像
make docker-build docker-push IMG=harbor.yuankeedu.com/aming/guestbook:v1
##如果编译不过去，那就是网络问题，下载镜像有问题，此时就要做一个代理
## 如下方法做代理
mkdir -p /etc/systemd/system/docker.service.d
cat > /etc/systemd/system/docker.service.d/proxy.conf <<EOF
[Service]
Environment="HTTP_PROXY=http://t.lishiming.net:38089/"
Environment="HTTPS_PROXY=http://t.lishiming.net:38089/"
Environment="NO_PROXY=localhost,127.0.0.1,.yuankeedu.com"
EOF
##注意，上面的地址要换成你自己的，这个代理是我自己设置的，如果你没有自己的代理，可以用我这个，但不保证一直能使用
systemclt daemon-reload
systemctl restart docerk 
```
**在k8s里部署该镜像**  
部署之前，需要把之前设置的代理取消，否则会出错
```bash
# 取消代理
unset http_proxy
unset https_proxy

# 修改kube-rbac-proxy镜像地址，因为自带的镜像下载不到
sed -i 's/gcr.io/gcr.lank8s.cn/' ./config/default/manager_auth_proxy_patch.yaml

# 在harbor可视化界面将项目改为公开，方便下载

# 在三个k8s node上手动将镜像下载下来
ctr -n k8s.io i pull harbor.yuankeedu.com/aming/guestbook:v1

# 部署，这是在k8s3上执行的，当前目录还是在$GOPATH/src/helloworld
make deploy IMG=harbor.yuankeedu.com/aming/guestbook:v1

# 查看pod
kubectl get po -n helloworld-system

# 此时，我们再次到k8s里去apply guestbook.yaml
kubectl delete -f guestbook.yaml
kubectl apply -f guestbook.yaml

# 再去查看helloworld-controller-manager-694854949d-wjkk5的log
kubectl -n helloworld-system logs  helloworld-controller-manager-694854949d-wjkk5
# 就能看到最后面的    Helloworld 输出了。
```
**清理**  
```bash
# 到k8s3，进入到$GOPATH/src/helloworld，执行
make uninstall
## 注意，它清理的是CRD资源，Controller并不会清理，要想删除Controller，直接删除对应ns即可
kubectl delete ns helloworld-system
```
参考：https://xinchen.blog.csdn.net/article/details/113089414

### Operator实战