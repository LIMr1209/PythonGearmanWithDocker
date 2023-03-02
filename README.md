##  使用Docker 搭建 Python Gearman 分布式任务调度

### 环境要求
- Docker
- Docker-Compose

### 启动
- Docker 启动 gearmand 服务 以及 Python gearman worker: 
  ```
  cd src
  docker-compose up
  docker-compose up -d  // 后台运行
  ```

### gearman 测试
-  进入Python docker 环境: 
```
  docker exec -it "python容器ID"  /bin/bash
  python gearman_client_test.py
```


### 监控 gearman
-  进入gearman docker 环境: 
```
  docker exec -it "gearmand容器ID"  /bin/bash
  watch -n 1 "(echo status; sleep 0.1) | nc 127.0.0.1 4730"
```

- 命令的结果会分为四列，它们的含义从左到右依次是：

- Function name: A string denoting the name of the function of the job
- Number in queue: A positive integer indicating the total number of jobs for this function in the queue. This includes currently running ones as well (next column)
- Number of jobs running: A positive integer showing how many jobs of this function are currently running
- Number of capable workers: A positive integer denoting the maximum possible count of workers that could be doing this job. Though they may not all be working on it due to other tasks holding them busy.

