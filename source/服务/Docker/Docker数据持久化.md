# Docker数据持久化
```bash
# 将本地目录映射到容器里
mkdir -p /data/
docker run -tid -v /data/:/data ubuntu bash
## -v 用来指定挂载目录 :前面的/data/为宿主机本地目录 :后面的/data/为容器里的目录，会在容器中自动创建

## 可以在/data/里创建一个文件
echo "hello" > /data/1.txt

## 然后到容器里查看
docker exec -it c82a5a00ae68 bash -c "cat /data/1.txt"
```
## 数据卷
```bash
# 创建数据卷（testvol为数据卷名字）
docker volume create testvol  

# 列出数据卷
docker volume ls

# 查看数据卷信息
docker volume inspect testvol

# 使用数据卷（和前面直接映射本地目录不同,冒号左边为数据卷名字）
docker run -itd --name linyi01 -v testvol:/data/ ubuntu

# 删除数据卷
docker volume rm testvol
```
```bash
# 将宿主机上的文件快速传输进容器里
docker cp /etc/fstab  linyi01:/tmp/test.txt
docker exec -it linyi01 cat /tmp/test.txt
```
