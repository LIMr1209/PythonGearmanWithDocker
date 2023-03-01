from gearman import JOB_UNKNOWN
from gearman.client import GearmanClient
from gearman import DataEncoder


def check_request_status(job_request):
    if job_request.complete:
        print("Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result))
    elif job_request.timed_out:
        print("Job %s timed out!" % job_request.unique)
    elif job_request.state == JOB_UNKNOWN:
        print("Job %s connection failed!" % job_request.unique)


client = GearmanClient(['gearmand:4730'])
# client = GearmanClient(['127.0.0.1:4730'])
completed_job_request = client.submit_job("reverse", "Hello World!")
check_request_status(completed_job_request)

# GearmanClient.get_job_status # 获取单个请求的作业状态
# GearmanClient.get_job_statuses # 获取多个请求的作业状态


import pickle


class PickleDataEncoder(DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return pickle.dumps(encodable_object)

    @classmethod
    def decode(cls, decodable_string):
        return pickle.loads(decodable_string)


class PickleExampleClient(GearmanClient):
    data_encoder = PickleDataEncoder

# my_python_object = {'hello': 'there'}
#
# gm_client = PickleExampleClient(['localhost:4730'])
# gm_client.submit_job("task_name", my_python_object)
