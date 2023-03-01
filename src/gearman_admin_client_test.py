from gearman.admin_client import GearmanAdminClient

admin_client = GearmanAdminClient(['gearmand:4730'])
# admin_client = GearmanAdminClient(['127.0.0.1:4730'])

admin_client.send_maxqueue("reverse", 100)  # 发送更改给定任务的最大队列大小的请求

# admin_client.send_shutdown()  # 发送关闭连接的gearman服务器的请求

# print(admin_client.get_version())  # 检索Gearman服务器的版本号

# admin_client.get_workers()  # 检索工作人员列表并报告他们正在执行的任务

# admin_client.ping_server()  # 发送调试字符串以在Gearman服务器上执行应用程序ping
