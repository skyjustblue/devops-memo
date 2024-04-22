# K8s里的API对象
在K8s里，YAML用来声明API对象的，那么API对象都有哪些？我们之前接触过的pod、deployment、service、node都是，当然还有好多，可以这样查看：  
```bash
kubectl api-resources
```


## 资源对象：pod
```bash
# 获取pod列表
kubectl get pods

# 运行一个pod
kubectl run pod-demo --image=busybox

# 查看pod详情
kubectl describe pod pod-demo

# 从已知Pod导出YAML文件
kubectl get pod pod-demo -o yaml  -o yaml > pod-demo.yaml
```
### pod yaml示例
四个核心部分：apiVersion、Kind、metadata、spec  
其他部分可以不用管，也可以删掉

```yaml
vim testpod.yaml

#手动创建一个pod，直接复制下面内容
apiVersion: v1
kind: Pod
metadata:
  name: ngx-pod
  namespace: linyi
  labels:  ## labels字段非常关键，它可以添加任意数量的Key-Value，目的是为了让pod的信息更加详细
    env: dev

spec:  ##用来定义该pod更多的资源信息，比如contain, volume, storage
  containers:  ##定义容器属性
  - image: nginx:1.23.2
    imagePullPolicy: IfNotPresent  ##镜像拉取策略，三种：Always/Never/IfNotPresent，一般默认是IfNotPresent，也就是说只有本地不存在才会远程拉取镜像，可以减少网络消耗。
    name: ngx
    env:  ##定义变量，类似于Dockerfile里面的ENV指令
      - name: os
        value: "Rocky Linux"
    ports:
    - containerPort: 80
```
```bash
# 上述配置文件中的namespace没有的话，需要创建，不然会报错
kubectl create namespace linyi

# 使用yaml文件创建pod
kubectl apply -f testpod.yaml

# 查看pod（po为简写）
[root@linyi k8s]# kubectl get po -n linyi
NAME      READY   STATUS    RESTARTS   AGE
ngx-pod   1/1     Running   0          102s

# 查看pod详情。（这里有个问题，如果在虚拟机做测试，虚拟机长期挂起会导致这个pod启动有问题，重启k8s解决或重启k8s后删除这个pod重新创建）
kubectl describe po ngx-pod -n linyi

# 删除pod
kubectl delete pod ngx-pod

# 删除namespace
kubectl delete namespace linyi
```

## 资源对象：Job
可以理解成一次性运行后就退出的Pod。

先来生成一个YAML文件：
```bash
kubectl create job job-demo --image=busybox  --dry-run=client  -o yaml > job-demo.yaml
```
```yaml
# 编辑此配置
vim job-demo.yaml

apiVersion: batch/v1
kind: Job
metadata:
  name: job-demo
spec:
  template:  ##模板，基于此模板来创建pod，它用来定义pod的属性，比如container
    spec:
      restartPolicy: OnFailure ##定义Pod运行失败时的策略，可以是OnFailure和Never，其中OnFailure表示失败的话需要重启容器，Never表示失败的话不重启容器，而是重新生成一个新的Pod
      containers:
      - image: busybox
        name: job-demo
        command: ["/bin/echo"]
        args: ["hellow", "world"]
```
```bash
# 创建job
kubectl apply -f job-demo.yaml

# 查看job
kubectl get job,pod

# 查看job详情
kubectl describe job job-demo

# 删除job
kubectl delete job job-demo
```
可以看到该容器运行完成后状态就变成了Completed。

对于Job，还有几个特殊字段：
- activeDeadlineSeconds，设置 Pod 运行的超时时间。
- backoffLimit，设置 Pod 的失败重试次数。
- completions，Job 完成需要运行多少个 Pod，默认是 1 个。
- parallelism，它与 completions 相关，表示允许并发运行的 Pod 数量，避免过多占用资源。

vi  myjob.yaml
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: sleep-job

spec:
  activeDeadlineSeconds: 15  #15s就超时
  backoffLimit: 2 #失败重试2次就放弃
  completions: 4 #要运行4个pod，才算完成
  parallelism: 2 #允许并发运行2个pod

  template:
    spec:
      restartPolicy: OnFailure
      containers:
      - image: busybox
        name: echo-job
        imagePullPolicy: IfNotPresent
        command:
          - sh
          - -c
          - sleep $(($RANDOM % 10 + 1)) && echo done  ##$(($RANDOM % 10 + 1))表示取1-10任意一个数字
```
```bash
# 创建job，并查看job情况
kubectl apply -f myjob.yaml ; kubectl get pod -w
```

## 资源对象：CronJob
CronJob简称（cj）是一种周期运行的Pod，比如有些任务需要每天执行一次，就可以使用CronJob。

先来生成一个YAML文件：
```bash
kubectl create cj cj-demo --image=busybox --schedule="" --dry-run=client  -o yaml > cj-demo.yaml
```
```yaml
# 编辑此配置
vim cj-demo.yaml

apiVersion: batch/v1
kind: CronJob
metadata:
  name: cj-demo

spec:
  schedule: '*/1 * * * *'
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - image: busybox
            name: cj-demo
            imagePullPolicy: IfNotPresent
            command: ["/bin/echo"]
            args: ["hello", "world"]
```
```bash
# 运行并查看
kubectl apply -f cj-demo.yaml
kubectl get cj
kubectl get pod
```

## 资源对象：ConfigMap
ConfigMap（简称cm）用来存储配置信息，比如服务端口、运行参数、文件路径等等。

示例：
```yaml
# 编辑配置
vim mycm.yaml

apiVersion: v1
kind: ConfigMap
metadata:
  name: mycm

data:
  DATABASE: 'db'
  USER: 'wp'
  PASSWORD: '123123'
  ROOT_PASSWORD: '123123'
```
```bash
# 创建cm
kubectl apply -f mycm.yaml

# 查看cm
kubectl get cm

# 查看cm详情
kubectl describe cm mycm

# 删除cm
kubectl delete cm mycm
```

在其它pod里引用ConfigMap：
```yaml
# 编辑配置
vim testpod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: testpod
  labels:
    app: testpod

spec:
  containers:
  - image: mariadb:10
    name: maria
    imagePullPolicy: IfNotPresent
    ports:
    - containerPort: 3306

    envFrom:   ##将cm里的字段全部导入该pod
    - prefix: 'MARIADB_'  ##将导入的字段名前面自动加上前缀，例如MARIADB_DATABASE， MARIADB_USER
      configMapRef:  ##定义哪个cm
        name: mycm
```
验证：
```bash
kubectl exec -it testpod -- bash
## 进入pod，查看变量$MARIADB_DATABASE
```

## 资源对象：Secret
Secret和cm的结构和用法很类似，不过在 K8s里Secret 对象又细分出很多类，比如：
- 访问私有镜像仓库的认证信息
- 身份识别的凭证信息
- HTTPS 通信的证书和私钥
- 一般的机密信息（格式由用户自行解释）  

前几种我们现在暂时用不到，所以就只使用最后一种。

示例：
```yaml
# 编辑配置
vim mysecret.yaml

apiVersion: v1
kind: Secret
metadata:
  name: mysecret

data:
  user: YW1pbmc=   ## echo -n "linyi"|base64
  passwd: bGludXgxMjM=  ## echo -n "test123"|base64
```
查看
```bash
kubectl apply -f mysecret.yaml
kubectl get secret
kubectl describe secret mysecret
```
在其它pod里引用Secret
```yaml
# 编辑配置
vim testpod2.yaml
apiVersion: v1
kind: Pod
metadata:
  name: testpod2

spec:
  containers:
  - image: busybox
    name: busy
    imagePullPolicy: IfNotPresent
    command: ["/bin/sleep", "300"]

    env:
      - name: USERNAME
        valueFrom:
          secretKeyRef:
            name: mysecret
            key: user
      - name: PASSWORD
        valueFrom:
          secretKeyRef:
            name: mysecret
            key: passwd
```
查看
```bash
kubectl exec -it testpod2 -- sh
## 进去后可以 echo $PASSWORD查看变量值
```

## 资源对象：Deployment
示例
```yaml
vim ng-deploy.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: myng
  name: ng-deploy
spec:
  replicas: 2 ##副本数
  selector:
    matchLabels:
      app: myng
  template:
    metadata:
      labels:
        app: myng
    spec:
      containers:
        - name: myng
          image: nginx:1.23.2
          ports:
          - name: myng-port
            containerPort: 80
```
matchLabels和labels之间的关系：  
![](2.png)  

```bash
# 使用YAML创建deploy
kubectl apply -f ng-deploy.yaml

# 查看deploy
kubectl get deploy

# 查看deploy详情
kubectl describe deploy ng-deploy

# 查看pod
kubectl get pod

# 删除deploy
kubectl delete deploy ng-deploy
```

## 资源对象：Service
Service（简称svc）是K8s集群中的一种资源对象，它定义了Pod的逻辑集合和访问该集合的策略。

示例：
```yaml
# 编辑配置
vim ng-svc.yaml

apiVersion: v1
kind: Service
metadata:
  name: ngx-svc
spec:
  selector:
    app: myng
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
```
```bash
# 使用YAML创建service
kubectl apply -f ng-svc.yaml

# 查看service
kubectl get svc

# 查看service详情
kubectl describe svc ngx-svc

# 删除service
kubectl delete svc ngx-svc
```

## 资源对象：Daemonset
有些场景需要在每一个node上运行Pod（比如，网络插件calico、监控、日志收集），Deployment无法做到，而Daemonset（简称ds）可以。Deamonset的目标是，在集群的每一个节点上运行且只运行一个Pod。  

Daemonset不支持使用kubectl create获取YAML模板，所以只能照葫芦画瓢了，参考Deployment的YAML编写，其实Daemonset和Deployment的差异很小，除了Kind不一样，还需要去掉replica配置。

示例：
```yaml
# 编辑配置
vim ds-demo.yaml

apiVersion: apps/v1
kind: DaemonSet
metadata:
  labels:
    app: ds-demo
  name: ds-demo
spec:
  selector:
    matchLabels:
      app: ds-demo
  template:
    metadata:
      labels:
        app: ds-demo
    spec:
      containers:
        - name: ds-demo
          image: nginx:1.23.2
          ports:
          - name: mysql-port
            containerPort: 80
```
```bash
# 使用YAML创建ds
kubectl apply -f ds-demo.yaml

# 查看ds
kubectl get ds

# 查看ds详情
kubectl describe ds ds-demo

# 查看pod
kubectl get pod

# 删除ds
kubectl delete ds ds-demo
```
但只在两个node节点上启动了pod，没有在master上启动，这是因为默认master有限制。
```bash
kubectl describe node k8s01 |grep -i 'taint'
Taints:             node-role.kubernetes.io/control-plane:NoSchedule
```
> 说明：  
> Taint叫做污点，如果某一个节点上有污点，则不会被调度运行pod。   
> 但是这个还得取决于Pod自己的一个属性：toleration（容忍），即这个Pod是否能够容忍目标节点是否有污点。  
> 为了解决此问题，我们可以在Pod上增加toleration属性，  
> 下面改一下YAML配置：
>  ```yaml
>  # 编辑配置
>  vim ds-demo.yaml
>
>  apiVersion: apps/v1
>  kind: DaemonSet
>  metadata:
>   labels:
>      app: ds-demo
>    name: ds-demo
>  spec:
>    selector:
>      matchLabels:
>        app: ds-demo
>    template:
>      metadata:
>        labels:
>          app: ds-demo
>      spec:
>        # 新增容忍污点
>        tolerations:
>          - key: node-role.kubernetes.io/control-plane
>            effect: NoSchedule
>        containers:
>          - name: ds-demo
>            image: nginx:1.23.2
>            ports:
>            - name: mysql-port
>              containerPort: 80
>
>
>  # 再次应用此YAML
>  kubectl apply -f ds-demo.yaml
>  ```


## 资源对象：Ingress/IngressClass
有了Service之后，我们可以访问这个Service的IP（clusterIP）来请求对应的Pod，但是这只能是在集群内部访问，要想实现外部访问，还需要额外的组件。  
![](./3.png)  
要想让外部用户访问此资源，可以使用NodePort，即在node节点上暴漏一个端口出来，但是这个非常不灵活。为了解决此问题，K8s引入了一个新的API资源对象Ingress，它是一个七层的负载均衡器，类似于Nginx。  
![](./4.png)  

三个概念：Ingress、Ingress Controller、IngressClass
- Ingress用来定义具体的路由规则，要实现什么样的访问效果；
- Ingress Controller是实现Ingress定义具体规则的工具或者叫做服务，在K8s里就是具体的Pod；
- IngressClass是介于Ingress和Ingress Controller之间的一个协调者，它存在的意义在于，当有多个Ingress Controller时，可以让Ingress和Ingress Controller彼此独立，不直接关联，而是通过IngressClass实现关联。  

![](5.png)  

Ingress YAML示例：
```yaml
# 编辑配置
vim mying.yaml

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: mying  ##ingress名字
  
spec:
  ingressClassName: myingc  ##定义关联的IngressClass
  
  rules:  ##定义具体的规则
  - host: linyi.com  ##访问的目标域名
    http:
      paths:
      - path: /
        pathType: Exact
        backend:  ##定义后端的service对象
          service:
            name: ngx-svc
            port:
              number: 80
```
```bash
# 查看ingress
kubectl get ing
kubectl describe ing mying
```

IngressClassYAML示例：
```yaml
# 编辑配置
vim myingc.yaml

apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: myingc

spec:
  controller: nginx.org/ingress-controller  ##定义要使用哪个controller
```
```bash
# 查看ingressclass
kubectl get ingressclass
kubectl describe ingressclass myingc
```

### 安装ingress-controller
使用Nginx官方提供的[ingress-controller](https://github.com/nginxinc/kubernetes-ingress)  

首先做一下前置工作
```bash
curl -O 'https://gitee.com/aminglinux/linux_study/raw/master/k8s/ingress.tar.gz'
tar zxf ingress.tar.gz
cd ingress
./setup.sh
##说明，执行这个脚本会部署几个ingress相关资源，包括namespace、configmap、secrect等
```
```yaml
# 编辑配置
vim ingress-controller.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: ngx-ing
  namespace: nginx-ingress

spec:
  replicas: 1
  selector:
    matchLabels:
      app: ngx-ing

  template:
    metadata:
      labels:
        app: ngx-ing
     #annotations:
       #prometheus.io/scrape: "true"
       #prometheus.io/port: "9113"
       #prometheus.io/scheme: http
    spec:
      serviceAccountName: nginx-ingress
      containers:
      #- image: nginx/nginx-ingress:2.2.0
      - image: nginx/nginx-ingress:2.2-alpine
        imagePullPolicy: IfNotPresent
        name: ngx-ing
        ports:
        - name: http
          containerPort: 80
        - name: https
          containerPort: 443
        - name: readiness-port
          containerPort: 8081
        - name: prometheus
          containerPort: 9113
        readinessProbe:
          httpGet:
            path: /nginx-ready
            port: readiness-port
          periodSeconds: 1
        securityContext:
          allowPrivilegeEscalation: true
          runAsUser: 101 #nginx
          capabilities:
            drop:
            - ALL
            add:
            - NET_BIND_SERVICE
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        args:
          - -ingress-class=myingc
          - -health-status
          - -ready-status
          - -nginx-status

          - -nginx-configmaps=$(POD_NAMESPACE)/nginx-config
          - -default-server-tls-secret=$(POD_NAMESPACE)/default-server-secret
```
```bash
# 应用YAML
kubectl apply -f ingress-controller.yaml

# 查看pod、deployment
kubectl get po -n nginx-ingress
kubectl get deploy -n nginx-ingress
```
测试：
```bash
# 将ingress对应的pod端口映射到master上临时测试
kubectl port-forward -n nginx-ingress ngx-ing-547d6575c7-fhdtt 8888:80 &  

# 测试前，可以修改ng-deploy对应的两个pod里的/usr/share/nginx/html/index.html文件内容，用于区分两个pod

# 测试访问
curl -x127.0.0.1:8888 linyi.com
## 或者：
curl -H 'Host:linyi.com' http://127.0.0.1:8888
```

## API资源对象PersistentVolume/PersistentVolumeClaim/StorageClass
持久化相关

三个概念：
- **PersistentVolume（pv）**：  
是对具体存储资源的描述，比如NFS、Ceph、GlusterFS等，通过pv可以访问到具体的存储资源；
+ **PersistentVolumeClaim（pvc）**：  
Pod想要使用具体的存储资源需要对接到pvc，pvc里会定义好pod希望使用存储的属性，通过pvc再去申请合适的存储资源（pv），匹配到合适的资源后pvc和pv会进行绑定，它们两者是一一对应的；
- **StorageClass（sc）**：  
pv可以手动创建，也可以自动创建，当pv需求量非常大时，如果靠手动创建pv就非常麻烦了，sc可以实现自动创建pv，并且会将pvc和pv绑定。  
sc对象会定义两部分内容：①pv的属性，比如存储类型、大小；②创建该pv需要用到的存储插件（provisioner），这个provisioner是实现自动创建pv的关键。

### 案例一（pv手动创建）

PV YAML示例：
```yaml
vi  testpv.yaml

apiVersion: v1
kind: PersistentVolume
metadata:
  name: testpv

spec:
  accessModes:
  - ReadWriteOnce
  capacity:
    storage: 500Mi  ##提供500Mi空间
  hostPath:
    path: /tmp/testpv/
```
说明：
accessModes定义该pv的访问权限模式，有三种：
- ReadWriteOnce：存储卷可读可写，但只能被一个节点上的 Pod 挂载;
- ReadOnlyMany：存储卷只读不可写，可以被任意节点上的 Pod 多次挂载;
- ReadWriteMany：存储卷可读可写，也可以被任意节点上的 Pod 多次挂载;

capacity 定义该存储大小。
hostPath 定义该存储访问路径。

PVC YAML示例：
```yaml
vi  testpvc.yaml

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: testpvc

spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi  ##期望申请100Mi空间
```
```bash
# 应用pv和pvc的YAML
kubectl apply -f testpv.yaml -f testpvc.yaml

# 查看状态
kubectl get pv,pvc
```
实验： 
将testpvc的期望100Mi改为1000Mi，查看pv的STATUS

### 案例二（pv通过sc自动创建）
为了更加贴近生产环境，需要先创建一个NFS服务器，然后通过NFS来演示sc的用法。

额外开一台虚拟机，搭建NFS服务（具体步骤略），假设NFS服务器IP地址为192.168.222.99，共享目录为/data/nfs

另外，要想使用NFS的sc，还需要安装一个NFS provisioner，它的作用是自动创建NFS的pv
github地址： https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner  

```bash
# 将源码下载下来
git clone https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner

cd nfs-subdir-external-provisioner/deploy

# 修改命名空间为kube-system
sed -i 's/namespace: default/namespace: kube-system/' rbac.yaml

# 创建rbac授权
kubectl apply -f rbac.yaml
```
```bash
# 修改命名空间为kube-system
sed -i 's/namespace: default/namespace: kube-system/' deployment.yaml

# 编辑deployment.yaml
vim deployment.yaml

   spec:
      serviceAccountName: nfs-client-provisioner
      containers:
        - name: nfs-client-provisioner
          image: chronolaw/nfs-subdir-external-provisioner:v4.0.2  ##改为dockerhub地址
          volumeMounts:
            - name: nfs-client-root
              mountPath: /persistentvolumes
          env:
            - name: PROVISIONER_NAME
              value: k8s-sigs.io/nfs-subdir-external-provisioner
            - name: NFS_SERVER
              value: 192.168.222.99  ##nfs服务器地址
            - name: NFS_PATH
              value: /data/nfs  ##nfs共享目录
      volumes:
        - name: nfs-client-root
          nfs:
            server: 192.168.222.99  ##nfs服务器地址
            path: /data/nfs  ##nfs共享目录
```
```bash
# 应用yaml
kubectl apply -f deployment.yaml 

# 创建storageclass
kubectl apply -f class.yaml
```

### SC YAML示例
```yaml
cat class.yaml

apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: nfs-client
provisioner: k8s-sigs.io/nfs-subdir-external-provisioner # or choose another name, must match deployment's env PROVISIONER_NAME'
parameters:
  archiveOnDelete: "false"  ##自动回收存储空间
```
有了SC，还需要一个PVC

### PVC
```yaml
vim nfs-pvc.yaml

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: nfs-pvc

spec:
  storageClassName: nfs-client
  accessModes:
    - ReadWriteMany

  resources:
    requests:
      storage: 500Mi
```


下面创建一个pod，来使用pvc：
```yaml
vim nfs-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: nfs-pod
spec:
  containers:
  - name: nfs-pod
    image: nginx:1.23.2
    volumeMounts:
    - name: nfspv
      mountPath: "/usr/share/nginx/html"
  volumes:
  - name: nfspv
    persistentVolumeClaim:
      claimName: nfs-pvc
```

**总结：**  
pod想使用共享存储 ---> PVC (定义具体需求属性） --->SC （定义Provisioner）---> Provisioner（定义具体的访问存储方法） ---> NFS-server  --->  自动创建PV

## API资源对象Statefulset
Pod的有状态和无状态：  
- 无状态：指的Pod运行期间不会产生重要数据，即使有数据产生，这些数据丢失了也不影响整个应用。比如Nginx、Tomcat等应用属于无状态。
- 有状态：指的是Pod运行期间会产生重要的数据，这些数据必须要做持久化，比如MySQL、Redis、RabbitMQ等。

Deployment和Daemonset适合做无状态，而有状态也有一个对应的资源，那就是Statefulset（简称sts）。

### Sts示例
```yaml
vim redis-sts.yaml

apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-sts

spec:
  serviceName: redis-svc ##这里要有一个serviceName，Sts必须和serice关联

  volumeClaimTemplates:
  - metadata:
      name: redis-pvc
    spec:
      storageClassName: nfs-client
      accessModes:
        - ReadWriteMany
      resources:
        requests:
          storage: 500Mi

  replicas: 2
  selector:
    matchLabels:
      app: redis-sts

  template:
    metadata:
      labels:
        app: redis-sts
    spec:
      containers:
      - image: redis:6.2
        name: redis
        ports:
        - containerPort: 6379

        volumeMounts:
        - name: redis-pvc
          mountPath: /data
```
```yaml
vim redis-svc.yaml

apiVersion: v1
kind: Service
metadata:
  name: redis-svc

spec:
  selector:
    app: redis-sts

  ports:
  - port: 6379
    protocol: TCP
    targetPort: 6379
```

```bash
# 应用两个YAML文件
kubectl apply -f redis-sts.yaml -f redis-svc.yaml
```
对于Sts的Pod，有如下特点：
- Pod名固定有序，后缀从0开始；
- “域名”固定，这个“域名”组成： Pod名.Svc名，例如 redis-sts-0.redis-svc；
- 每个Pod对应的PVC也是固定的；

**实验：**  
```bash
# ping 域名
kubectl exec -it redis-sts-0 -- bash
## 进去可以ping redis-sts-0.redis-svc 和  redis-sts-1.redis-svc
```
```bash
# 创建key
kubectl exec -it redis-sts-0 -- redis-cli

127.0.0.1:6379> set k1 'abc'
OK
127.0.0.1:6379> set k2 'bcd'
OK
```
```bash
# 模拟故障
kubectl delete pod redis-sts-0

## 删除后，它会自动重新创建同名Pod，再次进入查看redis key
kubectl exec -it redis-sts-0 -- redis-cli

127.0.0.1:6379> get k1
"abc"
127.0.0.1:6379> get k2
"bcd"
### 数据依然存在
```

## API资源对象Endpoint
Endpoint（简称ep）资源是和Service一一对应的，也就是说每一个Service都会对应一个Endpoint。
```bash
# 查看ep
kubectl get ep
NAME         ENDPOINTS                           AGE
kubernetes   192.168.222.131:6443                3d5h
ngx-svc      10.18.235.159:80,10.18.236.173:80   21h

# 查看service
kubectl get svc
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.15.0.1      <none>        443/TCP   3d5h
ngx-svc      ClusterIP   10.15.41.113   <none>        80/TCP    21h
```
Endpoint可以理解成Service后端对应的资源。

**有时候K8s里的Pod需要访问外部资源，比如访问外部的MySQL服务，就可以定义一个对外资源的Ednpoint，然后再定义一个Service，就可以让K8s里面的其它Pod访问了。**
```yaml
vim testep.yaml

apiVersion: v1
kind: Endpoints
metadata:
  name: external-mysql
subsets:
  - addresses:
    - ip: 192.168.222.99
    ports:
      - port: 3306

-----------------
apiVersion: v1
kind: Service  ##注意，该service里并不需要定义selector，只要Service name和Endpoint name保持一致即可
metadata:
  name: external-mysql
spec:
  ports:
    - port: 3306
```
```bash
# 应用
kubectl apply -f testep.yaml

# 查看
kubectl get ep
kubectl get svc
```
安装mariadb包（需要mysql命令），然后命令行连接Service external-mysql对应的Cluster IP测试

## API资源对象NetworkPolicy
NetworkPolicy用来控制Pod与Pod之间的网络通信，它也支持针对Namespace进行限制。基于白名单模式，符合规则的对象通过，不符合的拒绝。  

应用场景举例：
- Pod A不能访问Pod B；
- 开发环境所有Pod不能访问测试命名空间；
- 提供对外访问时，限制外部IP；

```yaml
# 官方NetworkPolicy YAML示例：

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - ipBlock:
            cidr: 172.17.0.0/16
            except:
              - 172.17.1.0/24
        - namespaceSelector:
            matchLabels:
              project: myproject
        - podSelector:
            matchLabels:
              role: frontend
      ports:
        - protocol: TCP
          port: 6379
  egress:
    - to:
        - ipBlock:
            cidr: 10.0.0.0/24
      ports:
        - protocol: TCP
          port: 5978
```
说明：
- 必需字段：apiVersion、 kind 和 metadata 字段。
- podSelector：定义目标Pod的匹配标签，即哪些Pod会生效此策略；
- policyTypes：表示给定的策略是应用于目标Pod的入站流量（Ingress）还是出站流量（Egress），或两者兼有。 如果NetworkPolicy未指定policyTypes则默认情况下始终设置Ingress。
- ingress：定义入流量限制规则，from用来定义白名单对象，比如网段、命名空间、Pod标签，Ports定义目标端口。
- egress：定义出流量限制规则，定义可以访问哪些IP和端口

### 案例一
**需求：**  
aming命名空间下所有Pod可以互相访问，也可以访问其他命名空间Pod，但其他命名空间不能访问aming命名空间Pod。

首先创建几个Pod：
```bash
# default命名空间里创建busybox Pod
kubectl run busybox --image=busybox -- sleep 3600

# aming命名空间里创建busybox Pod
kubectl run busybox --image=busybox -n aming -- sleep 3600

# aming命名空间里创建web pod
kubectl run web --image=nginx:1.23.2 -n aming
```
在没有创建NetworkPolicy的情况下测试
```bash
# aming命名空间的busybox ping default命名空间的busybox IP 
kubectl exec busybox -n aming -- ping 10.18.235.161

# aming命名空间的busybox ping aming命名空间的web IP
kubectl exec busybox -n aming -- ping 10.18.235.162

# default命名空间的busybox ping aming命名空间的web IP
kubectl exec busybox -- ping 10.18.235.162
```
创建networkpolicy的YAML
```yaml
vim deny-all-namespaces.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-namespaces
  namespace: aming
spec:
  podSelector: {} # 为空，表示匹配本命名空间所有Pod
  policyTypes:
  - Ingress
  ingress:
    - from:
      - podSelector: {} # 为空，表示匹配该命名空间所有Pod，即允许该命名空间所有Pod访问，没有定义namespaceSelector，也就是说不允许其它namespace的Pod访问。
```
应用YAML
```bash
kubectl apply -f deny-all-namespaces.yaml
```
测试
```bash
# aming命名空间的busybox ping default命名空间的busybox IP
kubectl exec busybox -n aming -- ping 10.18.235.161

# aming命名空间的busybox ping aming命名空间的web IP
kubectl exec busybox -n aming -- ping 10.18.235.162

# default命名空间的busybox ping aming命名空间的web IP
kubectl exec busybox -- ping 10.18.235.162


# 将刚刚创建的所有资源删除
kubectl delete po busybox  --force
kubectl delete po busybox -n aming --force
kubectl delete po web -n aming
kubectl delete -f deny-all-namespaces.yaml
```

### 案例二
通过PodSelector限制

```yaml
vim pod-selector.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-to-app
  namespace: aming
spec:
  podSelector:
    matchLabels:
      app: test
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: dev
      ports:
        - protocol: TCP
          port: 80
```
```bash
# 应用YAML
kubectl apply -f pod-selector.yaml
```
```bash
# 创建测试pod

# 创建Pod时，指定label
kubectl run web01 --image=nginx:1.23.2 -n aming -l 'app=test'  
# 查看label
kubectl get pod web01 -n aming --show-labels 
## 如果label创建错了，也可以修改，在本实验中不需要做如下操作
### kubectl label pod busybox app=test123 --overwrite 

kubectl run app01 --image=nginx:1.23.2 -n aming -l 'app=dev' 
kubectl run app02 --image=nginx:1.23.2 -n aming  
```
```bash
# 查看web01的IP
kubectl describe po web01 -n aming |grep -i ip

# 测试
kubectl exec -n aming app01 -- curl 10.18.235.170
kubectl exec -n aming app02 -- curl 10.18.235.170

# 测试成功后，删除掉刚刚创建的资源
kubectl delete po app01 -n aming
kubectl delete po app02 -n aming
kubectl delete po web01 -n aming
kubectl delete -f pod-selector.yaml
```

### 案例三
限制namespace
```yaml
vi allow-ns.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ns
  namespace: aming
spec:
  podSelector: {}
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: test
      ports:
        - protocol: TCP
          port: 80
```
```bash
# 应用YAML
kubectl apply -f allow-ns.yaml
```
```bash
# 创建测试ns 
kubectl create ns test

# 创建测试pod
kubectl run web01 --image=nginx:1.23.2 -n aming
kubectl run web02 --image=nginx:1.23.2 -n test
kubectl run web03 --image=nginx:1.23.2 
kubectl run web04 --image=nginx:1.23.2 -n aming

# 查看web01的IP
kubectl describe po web01 -n aming |grep -i ip

# 查看ns label
kubectl get ns --show-labels

# 给ns设置标签
kubectl label namespace test name=test

# 测试：
kubectl -n test exec web02 -- curl 10.18.235.172  #可以访问
kubectl exec web03 -- curl 10.18.235.172 #不可以访问
kubectl -n aming exec web04 -- curl 10.18.235.172  #不可以访问，即使同一个命名空间也无法访问
```
