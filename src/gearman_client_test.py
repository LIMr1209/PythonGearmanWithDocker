import time

from gearman import JOB_UNKNOWN
from gearman.client import GearmanClient
from util import JSONDataEncoder


class JsonClient(GearmanClient):
    data_encoder = JSONDataEncoder


def check_request_status(job_request):
    if job_request.complete:
        print("Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result))
    elif job_request.timed_out:
        print("Job %s timed out!" % job_request.unique)
    elif job_request.state == JOB_UNKNOWN:
        print("Job %s connection failed!" % job_request.unique)


# redis 做持久化队列
# docker run -itd -p 4730:4730  --name redis-gearmand --rm -i artefactual/gearmand:latest --queue-type=redis --redis-server=172.21.16.1 --redis-port=6379 --verbose=DEBUG


# client = GearmanClient(['gearmand:4730'])
client = JsonClient(['127.0.0.1:4730'])

# 单任务
# request = client.submit_job("json", "Hello World!", background=True)  # 异步 不会返回结果 存储结果 需要 worker 存到某一个介质中 （数据库，文件中）
# time.sleep(1)
# new_request = client.get_job_status(request)
# print(new_request.state)
# time.sleep(5)
# new_request = client.get_job_status(request)
# print(new_request.state)

# time.sleep(2)
# other_request = client.submit_job("json", "Hello 222!", background=True, unique=request.gearman_job.unique)  # 调用一个 已经存在的并且还在 运行的 unique 会忽略
# print(other_request)


# request = client.submit_job("json", "Hello World!", background=False) # 同步 等待返回结果
# print(request.result)


# request = client.submit_job("json", "Hello World!", background=True)
# print(request.result)

# 多任务
new_jobs = [
    dict(task='json', data={"hello": 'here'}),
    dict(task='json', data={'hello': 'there'}),
]

completed_requests = client.submit_multiple_jobs(new_jobs, background=True)  # 异步 不会返回结果
for current_request in completed_requests:
    check_request_status(current_request)

# 默认 max_retries 为 0 只能发送一次当前请求
# completed_requests = client.submit_multiple_jobs(new_jobs, background=False, max_retries=3) # 同步 等待返回结果
# for current_request in completed_requests:
#     check_request_status(current_request)
#
#     # 失败之后 重置 state  再次 发起请求 重试
#     current_request.state = JOB_UNKNOWN
#     client.send_job_request(current_request) # max_connection_attempts 4  最大连接次数 为 4    connection_attempts 当前连接次数 为 2
#     # 超过 最大连接  raise ExceededConnectionAttempts('Exceeded %d connection attempt(s) :: %r' % (current_request.max_connection_attempts, current_request))
#     check_request_status(current_request)


# 异步拿结果 方案

# GearmanClient.get_job_status # 获取单个请求的作业状态
# GearmanClient.get_job_statuses # 获取多个请求的作业状态

# 果有多个worker可以处理同一个function name, 则job server会自动分配一个
# background=True 后台运行
# inflight_request = client.submit_job("reverse_inflight", "Hello World!")
# 测试启动两个worker 处理该请求的 worker 挂掉 会切换到另一个worker 重新执行
# print(inflight_request.data_updates)  # 对应 worker.send_job_data
# print(inflight_request.status)  # 对应 worker.send_job_status
# print(inflight_request.warning_updates)  # 对应 worker.send_job_warning
