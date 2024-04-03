# API对象

## pod
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
# namespace没有的话，需要创建，不然会报错
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

