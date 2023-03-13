import datetime
import time
from gearman import GearmanWorker
from util import JSONDataEncoder
import sys


# worker 任务 处理过程中 发生异常  如果作业处于后台，则从队列中删除该作业
# 需要自己实现 异常捕获 重试操作 最大重试次数
# 超时 设置

class JsonWorker(GearmanWorker):
    data_encoder = JSONDataEncoder

    # def after_poll(self, any_activity):
    #     # After every select loop, let's rollback our DB connections just to be safe
    #     continue_working = True
    #     self.db_connections.rollback()
    #     return continue_working


def task_listener_json(gearman_worker, gearman_job):
    # print('json string: ' + gearman_job.data.decode("utf-8"))
    # return gearman_job.data.decode("utf-8")[::-1]
    print(datetime.datetime.now())
    print('Reversing object: ', gearman_job.data)
    # int("aa")
    time.sleep(3)
    return {"李振斌": gearman_job.data}


def task_listener_reverse_inflight(gearman_worker, gearman_job):
    reversed_data = reversed(gearman_job.data)
    total_chars = len(gearman_job.data)
    for idx, character in enumerate(reversed_data):
        time.sleep(1)
        print(total_chars)
        gearman_worker.send_job_data(gearman_job, str(character))  # 更新作业数据
        gearman_worker.send_job_status(gearman_job, idx + 1, total_chars)  # 更新作业状态
        gearman_worker.send_job_warning(gearman_job, str(idx + 1))  # 更新作业状态

    return None


worker = JsonWorker(['127.0.0.1:4730'])
# worker = JsonWorker(['gearmand:4730'])

worker.set_client_id('python-worker-' + sys.argv[1])  # 通知服务器我们应该被识别为这个客户端 ID
worker.register_task('json', task_listener_json)

# Enter our work loop and call gm_worker.after_poll() after each time we timeout/see socket activity
worker.work()  # 无限循环，完成来自所有连接的任务。

# worker.register_task('reverse_inflight', task_listener_reverse_inflight)
# GearmanWorker.unregister_task("reverse")  # 向 worker 注销函数
# GearmanWorker.send_job_data # 发送作业 数据 更新
# GearmanWorker.send_job_status # 发送作业状态 更新
# GearmanWorker.send_job_warning # 发送作业警告 更新
