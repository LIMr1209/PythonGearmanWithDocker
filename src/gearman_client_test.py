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


# client = GearmanClient(['gearmand:4730'])
client = JsonClient(['127.0.0.1:4730'])
# reverse_request = client.submit_job("reverse", "Hello World!")
# check_request_status(reverse_request)
# json_request = client.submit_job("json", {'hello': 'there'})
# check_request_status(json_request)


# 多任务
new_jobs = [
    dict(task='reverse', data='Hello World!'),
    dict(task='json', data={'hello': 'there'}),
]

completed_requests = client.submit_multiple_jobs(new_jobs)
for current_request in completed_requests:
    check_request_status(current_request)

# GearmanClient.get_job_status # 获取单个请求的作业状态
# GearmanClient.get_job_statuses # 获取多个请求的作业状态

# 果有多个worker可以处理同一个function name, 则job server会自动分配一个
# background=True 后台运行
# inflight_request = client.submit_job("reverse_inflight", "Hello World!")
# 测试启动两个worker 处理该请求的 worker 挂掉 会切换到另一个worker 重新执行
# print(inflight_request.data_updates)  # 对应 worker.send_job_data
# print(inflight_request.status)  # 对应 worker.send_job_status
# print(inflight_request.warning_updates)  # 对应 worker.send_job_warning
