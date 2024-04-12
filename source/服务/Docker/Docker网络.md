# Docker网络
Docker服务启动时会生成一个docker0的网卡，这个网卡是实现容器网络通信的根本。 默认容器使用的网络类型为桥接（bridge）模式，这个桥接和我们的vmware里的桥接可不是一回事。它更像是vmware的NAT模式。
每启动一个容器，都会产生一个虚拟网卡 vethxxx

`iptables -nvL -t nat`  可以看到DOCKER相关规则，容器之所以可以联网，是靠这些规则实现的

- host模式
    ```bash
    docker run -itd --net=host --name linyi03 ubuntu
    ```
    可以进入容器内，查看hostname，查看ip地址。 这种模式，容器和宿主机共享主机名、IP。

+ container模式  
该模式下，在启动容器时，需要指定目标容器ID或者name，意思是将要启动的容器使用和目标容器一样的网络，即它们的IP一样  
    ```bash
    docker run -itd --net=container:/linyi01 --name linyi04 ubuntu
    ```
    可以进入容器查看linyi01和linyi04的网络情况

- none模式  
即不需要配置网络  
    ```bash
    docker run -itd --net=none --name=linyi05 ubuntu_test bash

    # 查看
    docker exec -it linyi05 bash -c ip addr
    ```