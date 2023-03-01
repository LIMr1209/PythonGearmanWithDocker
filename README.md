##  使用Docker 搭建 Python Gearman 分布式任务调度

### 环境要求
- Docker

### 启动
- Docker 启动 gearmand 服务 以及 Python gearman worker: 
  ```
  cd src
  docker-compose up
  ``` 

### gearman 测试
-  进入Python docker 环境: 
```
  docker exec -it "python容器ID"  /bin/bash
  python gearman_client_test.py
```
