from gearman import GearmanWorker
from gearman import DataEncoder

gm_worker = GearmanWorker(['gearmand:4730'])
# gm_worker = GearmanWorker(['127.0.0.1:4730'])


def task_listener_reverse(gearman_worker, gearman_job):
    # gearman_job 参数
    print('Reversing string: ' + gearman_job.data.decode("utf-8"))
    return gearman_job.data.decode("utf-8")[::-1]


# gm_worker.set_client_id is optional
gm_worker.set_client_id('python-worker')  # 通知服务器我们应该被识别为这个客户端 ID
gm_worker.register_task('reverse', task_listener_reverse)  # 向这个 worker 注册一个函数

# Enter our work loop and call gm_worker.after_poll() after each time we timeout/see socket activity
gm_worker.work()  # 无限循环，完成来自所有连接的任务。


# GearmanWorker.unregister_task("reverse")  # 向 worker 注销函数
# GearmanWorker.send_job_data # 发送作业 数据 更新
# GearmanWorker.send_job_status # 发送作业状态 更新
# GearmanWorker.send_job_warning # 发送作业警告 更新


def task_listener_reverse_inflight(gearman_worker, gearman_job):
    reversed_data = reversed(gearman_job.data)
    total_chars = len(reversed_data)

    for idx, character in enumerate(reversed_data):
        gearman_worker.send_job_data(gearman_job, str(character))
        gearman_worker.send_job_status(gearman_job, idx + 1, total_chars)

    return None


import json


class JSONDataEncoder(DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return json.dumps(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        return json.loads(decodable_string)


class DBRollbackJSONWorker(GearmanWorker):
    data_encoder = JSONDataEncoder

    # def after_poll(self, any_activity):
    #     # After every select loop, let's rollback our DB connections just to be safe
    #     continue_working = True
    #     self.db_connections.rollback()
    #     return continue_working

# worker = DBRollbackJSONWorker(['gearmand:4730'])
